# Solutions

Example solutions (there may be others!)

# Exercise 2a

Find all the places it mentions bold support, and add equivalent support for italic.
In the final place where boldness is used to alter the "weight" of the text, you'll
need to do something else for italic. Read the line after that carefully and see if
you can see where italic is used.

# Exercise 4b

```
text = ""
num = random.randrange(0, 12)
for x in range(0, num):
    text += random.choice(["<tr>", "</tr>", "</td>", "<td>", "<table>", "</table>", "hello", "<th>", "</th>"])
return text
```

This should quite quickly generate:

```
<table>
<th>
some-data
```

which will cause a crash in the absence of a `<tr>` or `<td>`
