# Character generator

This program generates a number of random characters based on a provided database.

You are free to use the provided databases and definition files in the `db` directory for basic human parameters.

Not all generated values might make sense for now (for example it's possible to have a 2 years old have 3 children).

## Installation

Just download/clone the repository on your machine.

## Requirements

You will need Python 3.10 (or more recent) in order to run this software.
Once python is installed, you can run `pip` to install the requirements depicted in the `requirements.txt` file.

```
pip install -r requirements.txt
```

Running it once should be enough, and from time to time regarding library updates.

## Usage

If not installed as a python module, you can run the software with the given command from the parent directory of the python module:
```
python -m character-generator <definition-file> <db-files..>
```

You can also run `python -m character-generator --help` for full usage description.

## Database definition

### Types

- `percent`: the caracteristic is determined based on a percentage.
- `stack`: the presented odds are provided in a stacked value.
- `based`: the result of this can be based on actual statistics, only the actual result will be shown if there's no base value.
  If a value is provided, then the proportion will be made compared to its maximum.
- `either`: one key out of multiple has to be chosen. Keys are defined underneath, need to use "keys" attribute to list them and
  provide a default with `default_key`.
- `oneof`: picks a random entry from the values, which should be a list.

### Database values definition for stacks:

- `key`: a reference key for the value or its text if no "text" key is provided.
- `text` (opt): a text to be displayed for this value instead of the key.
- `chances`: chances of it happening (in %, or written "XX%")

The following definitions entries are all optional and are mutually exclusive:
- `cascade`: if this value is selected, triggers another generation for a given db entry, under the form: { db_key: number of times to be triggered }.
  A cascading entry will be appended after the current entry.
- `cascade_all_after`: similar to `cascade`, except this marks all following stack to cascade the db entries.
- `trigger`: similar to `cascade`, except this will add a new entry to the generated character.
- `trigger_all_after`: similar to `trigger`, except  this marks all following stack to trigger the db entries.

## Help

Check out the [wiki](https://github.com/Sylordis/character-generator/wiki).

## Authors

* Sylvain Domenjoud aka "[Sylordis](https://github.com/Sylordis)" (creator and maintainer)

## License

This project is licensed under the Apache License v2 - see the [LICENSE](LICENSE) file for details

## Links

Project website: <https://github.com/Sylordis/character-generator/>

# Issues

Issues are reported here: https://github.com/Sylordis/character-generator/issues
