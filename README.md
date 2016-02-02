![](https://raw.githubusercontent.com/arindampradhan/pok/master/poc-b.png)

# pok - Pocket CLI

| License | Version |
|---------|---------|
|[![license](https://img.shields.io/pypi/l/pok.svg)](https://github.com/arindampradhan/pok/blob/master/LICENSE)|[![version](https://img.shields.io/pypi/v/Pok.svg)](https://github.com/arindampradhan/pok/releases)|


## Why Use It

* Chrome extensions only gives saving options.
* Website looks complex, rarely access it.
* We use the mobile app.
* So, for desktop users.

![](https://raw.githubusercontent.com/arindampradhan/pok/master/poc-a.png)

## Features

- Written in simple Python   **[O_O]**
- Terminal friendly          **:)**
- All methods avaliable ``**add,delete,list items**``
- [Shell friendly](https://github.com/arindampradhan/pok#usage)
- Blazing tool to integrate with your Pocket
- Funny name                 **^_^**


## [Installation](https://pypi.python.org/pypi/pok)

    $ pip install pok


## Usage

![](https://raw.githubusercontent.com/arindampradhan/pok/master/poc-c.gif)

### :pouch: Basic Usage

**Retrive data**

    $ pok ls                # gives the titles and ids of pocket items

:bulb: **Note:** To get the links or urls from list use command in fullform. **`ls->list, sh->search, t->tag`**

    $ pok list              # gives the urls and the title of pockets items
    $ pok list 5            # you can also add a counter

### :pouch: Search

**Search via ``Name`` and ``Tag``**

    $ pok search google     # searches the url and the title of the pocket items

    $ pok tag django        # list items of the tag name django
    $ pok t python          # if you want to look at the ids of the pocket items


### :pouch: Modify

**``Delete`` and ``Add`` pocket item**

    $ pok delete <ID>       # deletes an pocket item

**You can find the ``<ID>`` from ``$ pok ls`` command**.

    $ pok push <url> <tags>  # Rarely going to use this.


**Adios**
