
# doit-indytasks

## install

```sh
pip install git+https://github.com/marcgardent/doit-indytasks.git
```

## Usage

```python

# dodo.py

## Import what you need
from dotasks.terraform import task_tf_plan

if __name__ == '__main__':
    import dotasks
    dotasks.run(globals())
    
```
