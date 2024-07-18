import feedparser
import pathlib
import re
from datetime import datetime

root = pathlib.Path(__file__).parent.resolve()


def replace_writing(content, marker, chunk, inline=False):
    r = re.compile(
        r'<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->'.format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = '\n{}\n'.format(chunk)
    chunk = '<!-- {} starts -->{}<!-- {} ends -->'.format(marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_writing():
    entries = feedparser.parse('https://alexsnow348.github.io/atom')['entries']
    top5_entries = entries[:5]
    entry_count = len(entries)
    return [
               {
                   'title': entry['title'],
                   'url': entry['link'].split('#')[0],
                   # change date to human readable format string to datetime object
                #    2024-04-04T00:00:00+00:00
                    'published': datetime.strptime(entry['updated'], "%Y-%m-%dT%H:%M:%S%z").strftime('%B %d, %Y')
               }
               for entry in top5_entries
           ], entry_count


if __name__ == '__main__':
    readme_path = root / 'README.md'
    readme = readme_path.open().read()
    entries, entry_count = fetch_writing()
    entries_md = '\n'.join(
        ['* [{title}]({url}) - {published}'.format(**entry) for entry in entries]
    )

    # Update entries
    rewritten_entries = replace_writing(readme, 'writing', entries_md)
    readme_path.open('w').write(rewritten_entries)

    # Update count
    readme = readme_path.open().read()  # Need to read again with updated entries
    rewritten_count = replace_writing(readme, 'writing_count', entry_count, inline=True)
    readme_path.open('w').write(rewritten_count)