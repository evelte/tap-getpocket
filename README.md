# tap-getpocket

`tap-getpocket` is a Singer tap for GetPocket.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

(If you are not running Meltano, see the instructions below to run this singer tap) 

To install this tap, go to your Meltano project folder. If you don't have a Meltano project yet, create one following 
the instructions [here](https://meltano.com/docs/getting-started.html#create-your-meltano-project).
From within your project, you can now add your custom tap:
```bash
meltano add --custom extractor tap-getpocket
```
You will be prompted to choose between one of the following options:
- PyPI package name:
    tap-getpocket
- Git repository URL:
    git+https://gitlab.com/meltano/tap-getpocket.git
- local directory, in editable/development mode:
    -e extract/tap-getpocket

This tap is available on PyPi, sou you can go with option 1 entering `tap-getpocket`.
If you want to use the git repository URL, enter `https://github.com/evelte/tap-getpocket`
Alternatively, download the package from github and provide the local path into option 3.

When prompted for capabilities and settings, enter the following:
```bash
(capabilities) [[]]: catalog,discover,state
(settings) [[]]: access_token:password,consumer_key:string,start_date:date_iso8601,favorite:boolean,state:string,detail_type:string,tag:string
```

See instructions on the configuration process [below](#Configuration).

### Running the Singer Tap without Meltano
Create and activate a Python 3 virtual environment for the tap (tap-getpocket)

```bash
python3 -m venv ~/.virtualenvs/tap-getpocket
source ~/.virtualenvs/tap-getpocket/bin/activate
# Install the Tap using pip:
pip install tap-getpocket
```

A full list of supported settings and capabilities for this tap is available by running:

```bash
tap-getpocket --about
```

Edit the Tap's config file (config.json) to include any necessary credentials or parameters. The file should look something like this:
```json
{
  "consumer_key": "xxxyourconsumerkeyxxx",
  "access_token": "xxxyouraccesstokenxxx",
  "favorite": true
}
```

This tap supports discovery mode, you can run it to obtain the catalog:

```bash
~/.virtualenvs/tap-getpocket/bin/tap-getpocket --config config.json --discover > catalog.json
``` 
Depending on what features the Tap supports, you may need to add metadata in the catalog for stream/field selection or replication-method.

Run the Tap in sync mode:

```bash
~/.virtualenvs/tap-getpocket/bin/tap-getpocket --config config.json --catalog catalog.json
```

The output should consist of SCHEMA, RECORD, STATE, and METRIC messages.
If you install a target, you can run the complete pipeline as follows:

```bash
~/.virtualenvs/tap-getpocket/bin/tap-getpocket | ~/.virtualenvs/target_jsonl/bin/target-jsonl --config config.json
```


## Configuration

### Accepted Config Options

There are 2 required config values to run this tap:
* `consumer_key`
* `access token`

A full list of supported settings and capabilities for this tap is available by running:
```bash
meltano invoke tap-getpocket --about
```

You can see your list of existing `consumer_key`s [here](https://getpocket.com/developer/apps/), after logging into your 
pocket account. You can use one of the available keys, or create a new one filling the form 
[here](https://getpocket.com/developer/apps/new/)

After getting your consumer_key, you can use the authentication script provided in the package `utils/authenticate.py`
in order to get your `access_token` to authenticate against the API service. You can also get the script 
[here](https://github.com/evelte/tap-getpocket/blob/master/utils/authenticate.py).

Optional settings to filter the results requested from the API include:
* start_date (The earliest record date to sync. Default is '2021-01-01T00:00:00Z')
* favorite (None, 0 or 1)
* state (unread, read or all)
* detail_type (basic or complete)
* tag (tag_name or _untagged_ for only items without tag)

If you are using Meltano you can add the settings directly on meltano.yml. You can see your current values running:
```bash
meltano config tap-getpocket list
```

## Usage

You can easily run `tap-getpocket` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-getpocket --version
tap-getpocket --help
tap-getpocket --config config.json --discover > ./catalog.json
```

## Developer Resources

- [ ] `Developer TODO:` As a first step, scan the entire project for the text "`TODO:`" and complete any recommended steps, deleting the "TODO" references once completed.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_getpocket/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-getpocket` CLI interface directly using `poetry run`:

```bash
poetry run tap-getpocket --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-getpocket
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-getpocket --version
# OR run a test `elt` pipeline:
meltano elt tap-getpocket target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.
