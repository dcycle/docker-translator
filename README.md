Translate files with [Microsoft Azure Translation](https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/quickstart/rest-api?tabs=csharp).

Usage
-----

* Make sure you have an Azure subscription at https://azure.microsoft.com/en-ca
* Go to the Azure Portal and create a Translators resource
* Go to resource and note the key and endpoint and location

Start by configuring your variables:

    export MS_ENDPOINT=https://api.cognitive.microsofttranslator.com/
    export MS_KEY=abc123abc123
    export MS_LOC=eastus

Then run a basic test, confirms everything works, you can run:

    ./scripts/test-ms.sh




    docker run --rm \
      -e ENDPOINT="$MS_ENDPOINT" \
      -e KEY="$MS_KEY" \
      -e LOC="$MS_LOC" \
      -v $(pwd)/example01:/data dcycle/ms-translate:1 \
      fr /data/example-en.md /data/example-fr.md

Adding the configuration to your profile file
-----

If you don't want to type in your configuration every time you use this, you can add your configuration to your `.zshenv` or `.bash_profile` files so they will be available every time you open a session.





See [this project on the Docker Hub](https://hub.docker.com/r/dcycle/ms-translate/).

More resources
-----

https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/quickstart/rest-api?tabs=csharp
