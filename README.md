# *yW2OO:* yWriter - OpenOffice/LibreOffice converter

For more information, see the [project homepage](https://peter88213.github.io/yW2OO) with description and download instructions.

## Development

*yw2OO* depends on the [pywriter](https://github.com/peter88213/PyWriter) library which must be present in your file system. It is organized as an Eclipse PyDev project. The official release branch on GitHub is *main*.

### Mandatory directory structure for building the application script

```
.
├── PyWriter/
│   └── src/
│       └── pywriter/
└── yw2OO/
    ├── src/
    ├── test/
    └── tools/ 
        └── build.xml
```

### Conventions

See https://github.com/peter88213/PyWriter/blob/main/docs/conventions.md

## Development tools

- [Python](https://python.org) version 3.9.
- [Eclipse IDE](https://eclipse.org) with [PyDev](https://pydev.org) and *EGit*.
- *Apache Ant* is used for building the application.

## Credits

The icons are made using the free *Pusab* font by Ryoichi Tsunekawa, [Flat-it](http://flat-it.com/).

## License

yW2OO is distributed under the [MIT License](http://www.opensource.org/licenses/mit-license.php).

