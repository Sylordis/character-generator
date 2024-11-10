# Character generator

This program generates a number of random characters based on a provided database.

You are free to use the provided databases and definition files in the `db` directory for basic human parameters.

Not all generated values might make sense for now (for example it's possible to have a 2 years old have 3 children).

## Installation

Just download/clone the repository on your machine.

## Requirements

You will need Python 3.10 (or more recent) in order to run this software.
Once python is installed, you can run `pip` to install the requirements depicted in the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

Running it once should be enough, and from time to time regarding library updates.

## Usage

If not installed as a python module, you can run the software with the given command from the parent directory of the python module:
```bash
python -m character-generator <definition-file> <db-files..>
```

You can also run `python -m character-generator --help` for full usage description.

**Example with samples:**

```bash
python -m character-generator character-generator/db/character_definition.yaml character-generator/db/db.yaml
```

## Traits database definition

The database is split in different documents, where each document is a "trait" that can be generated. Some trait may trigger the generation of other traits or may cascade into sub-categories of traits.

### Trait definition

```yaml
trait-name:
  name: display name of the trait
  type: [types]
  values:
  - values...
```

Values is according to the trait types.
See [trait types](#trait-types) or [values definition](#trait-values-definition-for-stacks) underneath.

### Trait definition with `type=either`

```yaml
trait-name:
  keys:
  - key 1
  - key 2
  - ...
  - key n
  default_key: key x (one of 1 to n)
  trait key 1 definition:
    ...
  trait key 2 definition:
    ...
  ...
  trait key n definition:
    ...
```

### Trait types

- `percent`: the caracteristic is determined based on a percentage.
- `stack`: the presented odds are provided in a stacked value, usually used with `percent`.
- `based`: the result of this can be based on actual statistics, only the actual result will be shown if there's no base value (ex: percentage if also `percent` type).
  If a value is provided, then the proportion will be made compared to its maximum.
- `either`: one key out of multiple has to be chosen. Keys are defined underneath, need to use `keys` attribute to list them and provide a default with `default_key` (see example upward).
- `oneof`: picks a random entry from the values, which should be a list.

### Trait values definition for stacks

- `key`: a reference key for the value or its text if no "text" key is provided.
- `text` (opt): a text to be displayed for this value instead of the key.
- `chances`: chances of it happening (in %, or written "XX%")
- `factor` (opt): 

The following definitions entries are all optional and are mutually exclusive:
- `cascade`: if this value is selected, triggers another generation for a given db entry, under the form: { db_key: number of times to be triggered }.
  A cascading entry will be appended after the current entry.
- `cascade_all_after`: similar to `cascade`, except this marks all following stack to cascade the db entries. `cascade` overrides a `cascade_all_after` for this given value.
- `trigger`: similar to `cascade`, except this will add a new entry to the generated character.
- `trigger_all_after`: similar to `trigger`, except  this marks all following stack to trigger the db entries. `trigger` overrides a `trigger_all_after` for this given value.

## Help

All the help is here. You can find sample files in the [db](db/) directory.

## Authors

* Sylvain Domenjoud aka "[Sylordis](https://github.com/Sylordis)" (creator and maintainer)

## License

This project is licensed under the Apache License v2 - see the [LICENSE](LICENSE) file for details

## Links

Project website: <https://github.com/Sylordis/character-generator/>

# Issues

Issues are reported here: https://github.com/Sylordis/character-generator/issues
