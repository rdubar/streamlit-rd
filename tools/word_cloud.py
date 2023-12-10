import os

from wordcloud import WordCloud

from settings import DATA_DIR

def create_word_cloud(text=False, show=False, save=True, filename=os.path.join(DATA_DIR, 'wordcloud.png')):

    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()

    # Read the whole text.
    if not text:
        text = open(os.path.join(DATA_DIR, 'library.txt')).read()

    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)

    if save:
        print(f'Saving wordcloud to {filename}')
        plt.imsave(filename, wordcloud)

    if show:
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()

        # The pil way (if you don't have matplotlib)
        # image = wordcloud.to_image()
        # image.show()

if __name__ == '__main__':
    create_word_cloud()