# Loripy

<img src="https://i.postimg.cc/Y2D6BW89/loripy.png" alt="drawing" heigth="300" width="300"/>

[![GitHub issues](https://img.shields.io/github/issues/qnbhd/loripy)](https://github.com/qnbhd/loripy/issues) [![GitHub forks](https://img.shields.io/github/forks/qnbhd/loripy)](https://github.com/qnbhd/loripy/network) [![GitHub stars](https://img.shields.io/github/stars/qnbhd/loripy)](https://github.com/qnbhd/loripy/stargazers) [![GitHub license](https://img.shields.io/github/license/qnbhd/loripy)](https://github.com/qnbhd/loripy/blob/master/LICENSE)

### Features

- Support anything documents
- Support numbers, string, variables. Soon for, if, built-in functions
- Rendering
- Pretty beatifulsoup4 docs reformat

## Run

Run loripy with manage script `python manage.py [TARGET] [DESTINATION]` for Windows

And `python3 manage.py [TARGET] [DESTINATION]` for Linux & MacOS

Or in code import loripy with `from import Loripy` 

and write:

```python
loripy = Loripy(filename, source_type='file')
```
where `filename` - source file, `source_type = 'file' or 'string'`

Next add needed variables and identifiers with
```python
loripy.sandbox.add_variable('var_name', var_value)
```

next write

```python
loripy.process()
loripy.render(destination)
```

Now render function open browser with rendered doc. 

## Language regulations

For start and end code block use `[$ <...> $]` where `<...>` some loripy code

Ordinary numbers, strings variables use.
For example:

`1.13`, `"string"`, `var_name`

## Examples

Input HTML-code with loripy

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>[$ var_name $]</title>
</head>
<body>
<h1>[$ "lorem ipsum" $]</h1>
<p>User name: [$ user_name $]</p>
</body>
</html>
```

where `var_name = 10` and `user_name = "qnbhd"`

Output code with loripy processing:


```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>10</title>
</head>
<body>
<h1>lorem ipsum</h1>
<p>User name: qnbhd</p>
</body>
</html>
```

With beautifulsoup formatting:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>
      10
    </title>
  </head>
  <body>
    <h1>
      lorem ipsum
    </h1>
    <p>
      User name: qnbhd
    </p>
  </body>
</html>
```



