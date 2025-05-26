Translate text or files with [Microsoft Azure Translation](https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/quickstart/rest-api?tabs=csharp).

Usage without Microsoft credentials
-----

To try this without valid credentials, using a simulator instead (which pseudo-translates, rather than translates, text), you can run:

    docker run --rm \
      -e MS_SIMULATE="true" \
      dcycle/translator:1 \
      preflight.py

This checks that our internal code is running correctly.

Usage with Microsoft credentials
-----

* Make sure you have an Azure subscription at https://azure.microsoft.com/en-ca
* Go to the Azure Portal and create a Translators resource
* Go to resource and note the key and endpoint and location

    docker run --rm \
      -e MS_ENDPOINT=https://api.cognitive.microsofttranslator.com/ \
      -e MS_KEY=abc123abc123 \
      -e MS_LOC=eastus \
      dcycle/translator:1 \
      preflight.py

Troubleshooting
-----

If the preflight does not work, double-check the error message and your credentials. If you are using the free tier, it might have expired and you might need to upgrade your subscription. Visit https://azure.microsoft.com/en-ca and make sure you subscription is active.

Adding the configuration to your profile file
-----

If you don't want to type in your configuration every time you use this, you can add your configuration to your `.zshenv` or `.bash_profile` files so they will be available every time you open a session. Something like this:

    # file ~/.zshenv or ~/.bash_profile
    ...
    export MS_ENDPOINT=https://api.cognitive.microsofttranslator.com/
    export MS_KEY=abc123abc123
    export MS_LOC=eastus

Now you can run:

    source ~/.zshenv

or

    ~/.bash_profile

And you can call your prelight like this:

    docker run --rm \
      -e MS_ENDPOINT="$MS_ENDPOINT" \
      -e MS_KEY="$MS_KEY" \
      -e MS_LOC="$MS_LOC" \
      dcycle/translator:1 \
      preflight.py

Your first translation
-----

Let's say you want to translate the sentence "La liberté commence où l'ignorance finit." from French to English, you can run:

    docker run --rm \
      -e MS_ENDPOINT="$MS_ENDPOINT" \
      -e MS_KEY="$MS_KEY" \
      -e MS_LOC="$MS_LOC" \
      dcycle/translator:1 \
      translate.py \
      --text "La liberté commence où l'ignorance finit." \
      --source-lang fr \
      --dest-lang en \
      --provider microsoft

You should get a response such as:

    Freedom begins where ignorance ends.

If you change your provider to "simulate", which is useful if you want to get a feel for how the system works without incurring costs, you will get the sentenced pseudo-translated by converted most vowels to the letter "a", like this:

    La labarté cammanca aù l'agnaranca fanat.

Ignoring certain parts of your text
-----

Let's say you translate the sentence "I met her on the ship The Queen of Egypt" to French, you will get a result:

    Je l’ai rencontrée sur le bateau La Reine d’Égypte.

But because The Queen of Egypt is the name of a ship, you might not want to translate it. The solution is to wrap it in `<span translate="no">...</span>`, like this:

    docker run --rm \
      -e MS_ENDPOINT="$MS_ENDPOINT" \
      -e MS_KEY="$MS_KEY" \
      -e MS_LOC="$MS_LOC" \
      dcycle/translator:1 \
      translate.py \
      --text 'I met her on the ship <span translate="no">The Queen of Egypt</span>.' \
      --source-lang en \
      --dest-lang fr \
      --provider microsoft

You'll now get:

    Je l’ai rencontrée sur le bateau <span translate="no">The Queen of Egypt</span>.

Processors
-----

Processors can change text before or after it is translated. Let's say you are happy with the translation `Je l’ai rencontrée sur le bateau <span translate="no">The Queen of Egypt</span>.`, but now that your text is translated, you want to remove the `<span translate="no">...</span>` part, you can use a post-processor for that, like this:

    docker run --rm \
      -e MS_ENDPOINT="$MS_ENDPOINT" \
      -e MS_KEY="$MS_KEY" \
      -e MS_LOC="$MS_LOC" \
      dcycle/translator:1 \
      translate.py \
      --text 'I met her on the ship <span translate="no">The Queen of Egypt</span>.' \
      --source-lang en \
      --dest-lang fr \
      --provider microsoft \
      --postprocessors '[{"name": "remove-span-translate-no-simple", "args": {}}]'

The result, now, will be:

    Je l’ai rencontrée sur le bateau The Queen of Egypt.

There are a number of built-in processors which you can see by looking at the source coe at ./docker-resources/my_translate.py and at the files at ./docker-resources/procesor_*.

It is not possible to add custom processors but that would eventually be nice to have.

Translating files
-----

Let's say you have a file at ./example01/file-file01.txt which contains:

    You’re mad. Bonkers. Off your head. But I’ll tell you a secret… all the best people are.

And you want to translate it to Spanish and put the result in a file called ./do-not-commit/file-file01.es.txt, you can use:

    docker run --rm \
      -e MS_ENDPOINT="$MS_ENDPOINT" \
      -e MS_KEY="$MS_KEY" \
      -e MS_LOC="$MS_LOC" \
      -v "$(pwd)":/data \
      dcycle/translator:1 \
      translate_file.py \
      --source /data/example01/file-file01.txt \
      --destination /data/do-not-commit/file-file01.es.txt \
      --source-lang en \
      --dest-lang es \
      --provider microsoft

Now, ./do-not-commit/file-file01.es.txt you will have:

    Estás loco. Loco. Fuera de tu cabeza. Pero te voy a contar un secreto... Todas las mejores personas lo son.

pre- and postprocessors work with files, as they do with text.

Translating markdown files with front matter
-----

When translating markdown files with front matter, you have access to some more features.

Front matter is anything between the lines with three dashes at the top of a file, for example consider a file which contains:

    ---
    title: "Quote: from Shakespeare's Hamlet"
    layout: quote
    lang: en
    ---
    There is nothing either good or bad, but thinking makes it so

The matter is structured information: the title, layout and language. The actual content of the file can appear below the front matter.

Let's try translating this file to French using the technique above:

    docker run --rm \
      -e MS_ENDPOINT="$MS_ENDPOINT" \
      -e MS_KEY="$MS_KEY" \
      -e MS_LOC="$MS_LOC" \
      -v "$(pwd)":/data \
      dcycle/translator:1 \
      translate_file.py \
      --source /data/example01/simple-frontmatter.md \
      --destination /data/do-not-commit/simple-frontmatter.fr.md \
      --source-lang en \
      --dest-lang fr \
      --provider microsoft

This yields:

    ---
    titre : « Citation: de Hamlet de Shakespeare »
    Mise en page : devis
    lang : en
    ---
    Il n’y a rien de bon ou de mauvais, mais c’est la pensée qui le rend ainsi.

In French, spaces are added before colons; and quotation marks are converted to « this format ».

Because front matter is in YAML format, this will break our file.

Furthermore, the keys in our front matter (title, layout, lang) should be preserved.

For all these purposes, a different technique can be used to translate markdown files with front matter:

    docker run --rm \
      -e MS_ENDPOINT="$MS_ENDPOINT" \
      -e MS_KEY="$MS_KEY" \
      -e MS_LOC="$MS_LOC" \
      -v "$(pwd)":/data \
      dcycle/translator:1 \
      translate_markdown.py \
      --source /data/example01/simple-frontmatter.md \
      --destination /data/do-not-commit/simple-frontmatter.fr.md \
      --source-lang en \
      --dest-lang fr \
      --provider microsoft \
      --preprocessors '[{"name": "translate-frontmatter", "args": {}}]' \
      --postprocessors '[{"name": "remove-span-translate-no", "args": {}}]'

This will yield:

    ---
    title: "Quote: from Shakespeare's Hamlet"layout: quotelang: fr
    translation:
      hash: 8bc3cc6d31bdb35f75985ad3d2e697e7
      message: "Translated by microsoft from en using http://github.com/dcycle/docker-translator on 2025-05-26"
    ---
    Il n’y a rien de bon ou de mauvais, mais c’est la pensée qui le fait.

This is good, but we would like the title to be translated. This can be achieved by:

    docker run --rm \
      -e MS_ENDPOINT="$MS_ENDPOINT" \
      -e MS_KEY="$MS_KEY" \
      -e MS_LOC="$MS_LOC" \
      -v "$(pwd)":/data \
      dcycle/translator:1 \
      translate_markdown.py \
      --source /data/example01/simple-frontmatter.md \
      --destination /data/do-not-commit/simple-frontmatter.fr.md \
      --source-lang en \
      --dest-lang fr \
      --provider microsoft \
      --preprocessors '[{"name": "translate-frontmatter", "args": {"translate": ["title"]}}]' \
      --postprocessors '[{"name": "remove-span-translate-no", "args": {}}]'

This will give you:

    ---
    title: "Citation : tirée de Hamlet de Shakespeare"
    layout: quote
    lang: fr
    translation:
      hash: 8bc3cc6d31bdb35f75985ad3d2e697e7
      message: "Translated by microsoft from en using http://github.com/dcycle/docker-translator on 2025-05-26"
    ---
    Il n’y a rien de bon ou de mauvais, mais c’est la pensée qui le fait.

which looks pretty good!

More resources
-----

* [Quickstart: Azure AI Translator REST APIs, 04/14/2025, Microsoft](https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/quickstart/rest-api?tabs=csharp)
