Here's a suitable fuzzer body.

```python
    html = ""
    for a in range(0, random.randrange(0,10)):
        if random.randrange(0, 2) > 0:
            html = html + "boo"
        else:
            tag = random.choice(["td","table","tr", "th"])
            ending = random.randrange(0, 2) > 0
            if ending:
                html = html + "</" + tag + ">"
            else:
                html = html + "<" + tag + ">"
    return html
```

This should quite quickly generate:

```
<table>
<th>
some-data
```

which will cause a crash in the absence of a `<tr>` or `<td>`
