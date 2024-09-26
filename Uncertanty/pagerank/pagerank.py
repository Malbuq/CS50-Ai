import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Initialise probability distribution dictionary:
    prob_dist = {page_name : 0 for page_name in corpus}

    # If page has no links, return equal probability for the corpus:
    if len(corpus[page]) == 0:
        for page_name in prob_dist:
            prob_dist[page_name] = 1 / len(corpus)
        return prob_dist

    # Probability of picking any page at random:
    random_prob = (1 - damping_factor) / len(corpus)

    # Probability of picking a link from the page:
    link_prob = damping_factor / len(corpus[page])

    # Add probabilities to the distribution:
    for page_name in prob_dist:
        prob_dist[page_name] += random_prob

        if page_name in corpus[page]:
            prob_dist[page_name] += link_prob

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    """
    pageRanks = dict()

    for key in corpus.keys():
        pageRanks[key] = 0
    
    curr_page = random.choice(list(corpus.keys()))
    pageRanks[curr_page] += 1/n

    for i in range(n-1):
        prob_next_pages = transition_model(corpus, curr_page, damping_factor)
        total_prob = 0
        curr_probability = random.random()

        for page in prob_next_pages.keys():
            total_prob += prob_next_pages[page]
            if curr_probability <= total_prob:
                curr_page = page
                break

        pageRanks[curr_page] += 1/n

    return pageRanks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages_corpus = len(corpus)
    page_ranks = {page: (1 / total_pages_corpus) for page in corpus}

    for i in range(SAMPLES):
        


def PR(page, corpus):
    count_linked_pages = len(corpus[page])
    first_condition = (1 - DAMPING) / count_linked_pages
    somatory = 0

    if count_linked_pages == 0:
        for curr_page in corpus:
            somatory += (PR(curr_page, corpus)) / len(corpus)

        second_condition = DAMPING * somatory

        return (first_condition + second_condition)
            
    for curr_page in corpus[page]:
        somatory += (PR(curr_page, corpus)) / len(corpus[curr_page])

    second_condition = DAMPING * somatory

    return (first_condition + second_condition)



if __name__ == "__main__":
    main()
