import os
import random
import re
import sys
import copy

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
    pr = dict()
    number_of_pages = len(corpus)
    number_of_links = len(corpus[page])

    if number_of_links != 0:
        links_of_page = corpus[page]
        pr[page] = (1-damping_factor)/number_of_pages

        for i in links_of_page:
            pr[i] = (damping_factor/number_of_links) + pr[page]
        
        return pr
    
    for i in corpus:
        pr[i] = 1/number_of_pages
    
    return pr


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr = dict()
    new_pr = dict()
    for item in corpus:
        pr[item] = 1/len(corpus)
    for i in range(n):
        page = random.choices(list(pr.keys()), list(pr.values()), k=1)[0]
        new_pr[page] = new_pr.get(page, 0) + 1
        pr = transition_model(corpus, page, damping_factor)
    for item in new_pr:
        new_pr[item] = new_pr[item]/n
    
    return new_pr
        


def linksto_page(corpus, page):
    links = set()
    for item in corpus:
        if page in corpus[item]:
                links.add(item)
    return links

def converged(old_pr, new_pr):
    diff = 0.001
    for page in old_pr:
        if abs(old_pr[page] - new_pr[page]) > diff:
            return False
    return True


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr = dict()
    N = len(corpus)
    has_converged = False

    for item in corpus:
        pr[item] = 1/N
    
    while not has_converged:
        old_pr = copy.deepcopy(pr)
        for page in old_pr:
            links = linksto_page(corpus,page)
            links_total_pr = 0
            for i in links:
                links_total_pr+= old_pr[i]

            pr[page] = (1-damping_factor)/N + damping_factor * (links_total_pr/len(links))
        has_converged = converged(old_pr, pr)
    return pr
    


if __name__ == "__main__":
    main()
