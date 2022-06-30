from leetscraper import Leetscraper

if __name__ == "__main__":
    websites = ["leetcode.com",
                "projecteuler.net",
                "codechef.com",
                "hackerrank.com",
                "codewars.com"]
    for site in websites:
        Leetscraper(website_name=site)
