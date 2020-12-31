import feedparser
import pathlib
import re

rssUrl = "https://blog.monsterx.cn/feed.xml"
startMark = r"<!-- posts start -->"
endMark = r"<!-- posts end -->"
NUM = 5

def update_readme(start, end, repl):
    # Splicing complete regular expressions
    pattern = re.compile(
        r"(?<=(" + start + r")).*(?=(" + end + r"))",
        re.DOTALL,
    )
    # Get contents and rewrite README.md
    readme = pathlib.Path(__file__).parent.resolve() / "README.md"
    readme_contents = readme.open().read()
    readme.open("w").write(pattern.sub('\n' + repl + '\n', readme_contents))

def fetch_posts(url):
    blog = feedparser.parse(url)
    posts = blog['entries']
    markdown = "\n"
    # Fetch only 5 latest posts' info
    # My post.published return "Tue, 30 Jun 2020 00:00:00 GMT"
    # So I just intercept the middle part of the character
    for post in posts[:NUM]:
        # markdown += " ※ 《[" + post.title + "](" + post.link + ")》" + post.published + "<br />\n"
        markdown += " - 《[" + post.title + "](" + post.link + ")》    " + post.published[5:16] + "<br />\n"
    #markdown += "\n\n [Read more..](" + blog['feed']['link'] + ")\n"
    return markdown

if __name__ == "__main__":
    postsNew = fetch_posts(rssUrl)
    update_readme(startMark, endMark, postsNew)
