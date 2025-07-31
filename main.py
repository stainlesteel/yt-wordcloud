from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled, VideoUnavailable
# ^ imports for yt 
from rich import print
from rich.console import Console
# ^ imports for make terminal look cool
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# ^ imports for generating wordcloud and displaying image

langs = ['en', 'en-US', 'en-GB', 'en-auto']
# ^ base languages for ytt-api
def fetch(): # fetches subs for video, along with pre processing
    global txt3
    try:
      api = YouTubeTranscriptApi()
      data = api.fetch(res_id, langs)
      print("[cyan]Fetching...[/cyan]")
      segs = [item.text for item in data]
      print("[turquoise4]Pre-processing[/turquoise4]")
      txt = " ".join(segs)
      txt2 = txt.replace('""', '')
      txt3 = txt2.replace('.', '')
      save()
      wordcloud()
    except NoTranscriptFound:
        print(f"[bold red]Error: This video does not contain any english subtitles (en, en-US, en-GB, en-auto)[/bold red]")
    except TranscriptsDisabled:
        print(f"[bold red]Error: This video does not allow subtitles.[/bold red]")
    except VideoUnavailable:
        print(f"[bold red]Error: This video isn't available.[/bold red]")
        print("Common mistakes:")
        print("1. Using a youtu.be link, do not do this, and provide the youtube.com link.")
        print("2. Most links may have a '&t=s' or something similar at the end. If so, remove it and try again.")

def wordcloud(): # generates wordcloud, shows image and saves
    wc = WordCloud()
    wc.generate(txt3)
    wc.to_file(f"{res_id}.png")
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    print("Here's your image!. If you're on [yellow]Linux[/yellow], prepare for Wayland/X11 warnings!")
    plt.show()
    print("Image of wordcloud and txt of subtitle have been saved!")
    

def save(): # saves the subs as txt
    global txt3
    global res_id
    with open(f'{res_id}.txt', 'w') as txt:
         txt.write(txt3)

def main():
    global res_id
    cons = Console()
    cons.clear(home=True)
    print("Welcome to [red]yt-wordcloud[/red].")
    id = cons.input("Provide the [red]youtube[/red] video [purple]id/URL[/purple]: ")
    if "v=" in id:
        id_start = "v="
        if "&" in id:
            cat_id = id.split(id_start, 1)[1]
            qwe_id = cat_id.split('&')
            res_id = qwe_id[0]
            print(f"id is: {res_id}")
        else:    
            res_id = id.split(id_start, 1)[1]
            print(f"id is: {res_id}")
    else:
        res_id = id
        print(f"id is {res_id}")
    fetch()

main()
