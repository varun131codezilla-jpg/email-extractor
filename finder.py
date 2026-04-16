import os
import sys
import re
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MasterEmailFinder:
    def __init__(self, first_name, last_name, domain):
        self.first_name = first_name.strip().lower()
        self.last_name = last_name.strip().lower()
        self.domain = domain.strip().lower()
        self.api_key = os.getenv("SERPER_API_KEY")
        self.search_url = "https://google.serper.dev/search"
        
        if not self.api_key:
            raise ValueError("SERPER_API_KEY not found in environment variables.")

    def _google_search(self, query):
        payload = json.dumps({"q": query, "num": 20})
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(self.search_url, headers=headers, data=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Error during Google Search: {e}")
            if e.response is not None:
                print(f"Response context: {e.response.text}")
            return {}
        except requests.exceptions.RequestException as e:
            print(f"Error during Google Search: {e}")
            return {}

    def _extract_emails(self, text):
        # Basic regex to find emails matching the domain
        pattern = r'[a-zA-Z0-9.\-_]+@' + re.escape(self.domain)
        return re.findall(pattern, text)

    def _get_text_from_results(self, results):
        text_snippets = []
        if 'organic' in results:
            for item in results['organic']:
                text_snippets.append(item.get('snippet', ''))
                text_snippets.append(item.get('title', ''))
        return " ".join(text_snippets).lower()

    def tier_1_exact_match(self):
        print("Executing Tier 1: Exact Match Search...")
        query = f'"{self.first_name} {self.last_name}" "@{self.domain}" email'
        results = self._google_search(query)
        text = self._get_text_from_results(results)
        emails = self._extract_emails(text)
        
        # Look for combinations of first and last name in the email
        possible_emails = self.tier_3_permutations()
        
        for email in emails:
            email = email.lower()
            if email in possible_emails:
                return email
                
            # As a fallback, if we find any email near the person's name, 
            # and it's not a generic email, we could return it.
            username = email.split('@')[0]
            if self.first_name in username or self.last_name in username:
                return email
        
        return None

    def tier_2_format_deduction(self):
        print("Executing Tier 2: Format Deduction...")
        query = f'*@{self.domain}'
        results = self._google_search(query)
        text = self._get_text_from_results(results)
        emails = set(self._extract_emails(text))
        
        generic_prefixes = ['info', 'contact', 'sales', 'support', 'press', 'marketing', 'hello', 'jobs', 'careers']
        
        for email in emails:
            username = email.split('@')[0]
            if username in generic_prefixes:
                continue
            
            # Deduce format
            if '.' in username:
                parts = username.split('.')
                if len(parts) == 2:
                    if len(parts[0]) == 1:
                        format_guessed = f"{self.first_name[0]}.{self.last_name}@{self.domain}"
                        print(f"  Deducing format f.last from {email}")
                        return format_guessed
                    else:
                        format_guessed = f"{self.first_name}.{self.last_name}@{self.domain}"
                        print(f"  Deducing format first.last from {email}")
                        return format_guessed
        
        return None

    def tier_3_permutations(self):
        print("Executing Tier 3: Permutation Generation...")
        return [
            f"{self.first_name}.{self.last_name}@{self.domain}",
            f"{self.first_name[0]}.{self.last_name}@{self.domain}",
            f"{self.first_name[0]}{self.last_name}@{self.domain}",
            f"{self.first_name}{self.last_name[0]}@{self.domain}",
            f"{self.first_name}@{self.domain}"
        ]

    def find_email(self):
        # Tier 1
        email = self.tier_1_exact_match()
        if email:
            print(f"[Tier 1 Success] Found exact match: {email}")
            return {"email": email, "tier": 1}
        
        # Tier 2
        email = self.tier_2_format_deduction()
        if email:
            print(f"[Tier 2 Success] Deduced format from other employees: {email}")
            return {"email": email, "tier": 2}
        
        # Tier 3
        emails = self.tier_3_permutations()
        print(f"[Tier 3 Fallback] Generated permutations: {', '.join(emails)}")
        return {"emails": emails, "tier": 3}

if __name__ == "__main__":
    if len(sys.argv) == 4:
        first, last, domain = sys.argv[1:4]
    else:
        first, last, domain = "Sam", "Altman", "openai.com"
        print("Usage: python finder.py <first_name> <last_name> <domain>")
        print(f"Falling back to default: {first} {last} @ {domain}\n")
        
    finder = MasterEmailFinder(first, last, domain)
    result = finder.find_email()
    print("\n--- Final Result ---")
    print(json.dumps(result, indent=2))
