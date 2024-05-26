function ensureHttpScheme(url) {
    if (!url.startsWith("http://") && !url.startsWith("https://")) {
        return "https://" + url;
    }
    return url;
}

function fetchRobotsTxt(url) {
    // Using a CORS proxy
    const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
    return fetch(proxyUrl + url + '/robots.txt')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.text();
        });
}

function findSitemapsInRobots(robotsContent) {
    const regex = /Sitemap: (.+)/gi;
    let match;
    const sitemaps = [];
    while ((match = regex.exec(robotsContent)) !== null) {
        sitemaps.push(match[1]);
    }
    return sitemaps;
}

function checkSitemap(url) {
    // Using a CORS proxy
    const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
    return fetch(proxyUrl + url, { method: 'HEAD' })
        .then(response => response.ok)
        .catch(() => false);
}

function findSitemapInHtml(url) {
    // Using a CORS proxy
    const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
    return fetch(proxyUrl + url)
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch page');
            return response.text();
        })
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");
            const links = doc.querySelectorAll('a[href]');
            const sitemaps = [];
            links.forEach(link => {
                if (link.href.toLowerCase().includes('sitemap')) {
                    sitemaps.push(link.href);
                }
            });
            return sitemaps;
        });
}

function searchForSitemaps() {
    const url = ensureHttpScheme(document.getElementById('urlInput').value.trim());
    const resultContainer = document.getElementById('result');
    resultContainer.textContent = 'Searching for sitemaps, please wait...';

    fetchRobotsTxt(url)
        .then(content => {
            const sitemaps = findSitemapsInRobots(content);
            return Promise.all(sitemaps.map(sitemapUrl => checkSitemap(sitemapUrl).then(isValid => isValid ? sitemapUrl : null)));
        })
        .then(results => {
            const validSitemaps = results.filter(result => result !== null);
            if (validSitemaps.length > 0) {
                resultContainer.textContent = `Sitemap found: ${validSitemaps.join(', ')}`;
            } else {
                // If no sitemap found in robots.txt, search in HTML
                return findSitemapInHtml(url).then(htmlSitemaps => {
                    const validHtmlSitemaps = htmlSitemaps.filter(sitemap => sitemap !== null);
                    resultContainer.textContent = validHtmlSitemaps.length > 0 ? `Sitemap found in HTML: ${validHtmlSitemaps.join(', ')}` : 'No accessible Sitemap found using all methods.';
                });
            }
        })
        .catch(error => {
            resultContainer.textContent = 'Error fetching or processing: ' + error.message;
        });
}

document.getElementById('urlInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        searchForSitemaps();
    }
});
