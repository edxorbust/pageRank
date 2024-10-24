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
        item = item/n
    
    return new_pr

corpus = {a:{a,b,c}, b:{a,c}, c:{d}, d:{a,b}}
damping_factor = 0.85
n = 1000