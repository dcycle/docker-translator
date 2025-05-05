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

    ./scripts/preflight.sh

Adding the configuration to your profile file
-----

If you don't want to type in your configuration every time you use this, you can add your configuration to your `.zshenv` or `.bash_profile` files so they will be available every time you open a session.

Translate markdown files from one language to another, preserving frontmatter
-----

Add a file in ./example01 which has the title "test-file.md" and the following contents:

    ---
    title: "This should be translated"
    something:
    - whatever: This should be translated
    something_else: "This should be translated"
    this_is_the_language_key: en
    ---
    This should be translated

        This should not be translated because it is preceded by four spaces and is code
        // This should be translated because it is a comment

Make a script called ./scripts/translate-md.sh

It should be possible to call it like this:

    mkdir ./do-not-commit

    ./scripts/translate-md.sh \
      --source example01/test-file.md \
      --langkey this_is_the_language_key \
      --source-lang en \
      --dest-lang fr \
      --destination-folder do-not-commit \
      --provider simulate \
      --translate-key translation_info_key \
      --translate-message "Translated by @provider from @source using @repo on @date"

The arguments to ./scripts/translate-md.sh can have sensible defaults

    --source (no default)
    --langkey default is lang
    --source-lang (no default)
    --dest-lang (no default)
    --destination-folder default is same as source
    --provider default is microsoft
    --translate-key default is translation
    --translate-message default is "Translated by @Provider from @source using @repo on @Date"
    --do-not-translate-frontmatter (no default, by default every frontmatter key is translated)

When you run this, it should result in the following file appearing:

    ./do-not-commit/translate-md-fr.sh

example:-

    ./scripts/translate-md.sh \
      --source example01/test-file.md \
      --langkey this_is_the_language_key \
      --source-lang en \
      --dest-lang fr \
      --destination-folder do-not-commit \
      --provider simulate \
      --translate-key translation_info_key \
      --translate-message "Translated by @provider from @source using @repo on @date" \
      --do-not-translate-regex \
      --remove-span-translate-no


    ./scripts/translate-md.sh \
      --source example01/test-file.md \
      --langkey this_is_the_language_key \
      --source-lang en \
      --dest-lang fr \
      --destination-folder do-not-commit \
      --provider simulate \
      --translate-key translation_info_key \
      --translate-message "Translated by @provider from @source using @repo on @date" \
      --do-not-translate-frontmatter '["title", "something", "whatever"]' \
      --do-not-translate-regex \
      --remove-span-translate-no

Force if same hash parameter
-----
    During development if you would like to be able to overwrite the translated file if necessary then
    use --force-if-same-hash parameter in the command.

    ```
    ./scripts/translate-md.sh --source example01/test-file.md \
        --langkey this_is_the_language_key \
        --source-lang en \
        --dest-lang fr \
        --destination-folder do-not-commit \
        --provider simulate \
        --translate-key translation_info_key \
        --translate-message "Translated by @provider from @source using @repo on @date" \
        --do-not-translate-frontmatter '["title", "something", "whatever"]' \
        --do-not-translate-regex \
        --remove-span-translate-no \
        --force-if-same-hash
    ```


More resources
-----

* [Quickstart: Azure AI Translator REST APIs, 04/14/2025, Microsoft](https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/quickstart/rest-api?tabs=csharp)
