#include "ctrees.h"
#include <Python.h>

#define LEFT 0
#define RIGHT 1
#define KEY(node) (node->key)
#define VALUE(node) (node->value)
#define LEFT_NODE(node) (node->link[LEFT])
#define RIGHT_NODE(node) (node->link[RIGHT])
#define LINK(node, dir) (node->link[dir])
#define XDATA(node) (node->xdata)
#define RED(node) (node->xdata)
#define BALANCE(node) (node->xdata)

node_t *ct_new_node(PyObject *key, PyObject *value, int xdata)
{
  node_t *new_node = PyMem_Malloc(sizeof(node_t));
  if (new_node != NULL)
    {
      KEY(new_node) = key;
      Py_INCREF(key);
      VALUE(new_node) = value;
      Py_INCREF(value);
      LEFT_NODE(new_node) = NULL;
      RIGHT_NODE(new_node) = NULL;
      XDATA(new_node) = xdata;
    }
  return new_node;
}

void ct_delete_node(node_t *node)
{
  if (node != NULL)
    {
      Py_XDECREF(KEY(node));
      Py_XDECREF(VALUE(node));
      LEFT_NODE(node) = NULL;
      RIGHT_NODE(node) = NULL;
      PyMem_Free(node);
    }
}

void ct_delete_tree(node_t *root)
{
  if (root == NULL) return;
  if (LEFT_NODE(root) != NULL)
    {
      ct_delete_tree(LEFT_NODE(root));
    }
  if (RIGHT_NODE(root) != NULL)
    {
      ct_delete_tree(RIGHT_NODE(root));
    }
  ct_delete_node(root);
}

void ct_swap_data(node_t *node1, node_t *node2)
{
  PyObject *tmp;
  tmp = KEY(node1);
  KEY(node1) = KEY(node2);
  KEY(node2) = tmp;
  tmp = VALUE(node1);
  VALUE(node1) = VALUE(node2);
  VALUE(node2) = tmp;
}

int ct_compare(PyObject *compare, PyObject *key1, PyObject *key2)
{
  // Invoke a Python compare function returning the result as an int.
  PyObject *res;
  PyObject *args;
  int i;

  args = PyTuple_New(2);
  if (args == NULL)
    return -1;
  Py_INCREF(key1);
  Py_INCREF(key2);
  PyTuple_SET_ITEM(args, 0, key1);
  PyTuple_SET_ITEM(args, 1, key2);
  res = PyObject_Call(compare, args, NULL);
  Py_DECREF(args);
  if (res == NULL) return -1; // get no result object, compare is not callable?
  if (!PyInt_Check(res)) {
    Py_DECREF(res);
    PyErr_SetString(PyExc_TypeError, "comparison function must return int");
    return -1;
  }
  i = PyInt_AsLong(res);
  Py_DECREF(res);
  return i;
}

node_t *ct_find_node(node_t *root, PyObject *key, PyObject *cmp)
{
  int res;
  while(root != NULL)
    {
      res = ct_compare(cmp, key, KEY(root));
      if (res == 0) // key found
        return root;
      else
        root = LINK(root, (res > 0));
    }
  return NULL; // key not found
}

PyObject *ct_get_item(node_t *root, PyObject *key, PyObject *cmp)
{
  node_t *node;
  PyObject *tuple;

  node = ct_find_node(root, key, cmp);
  if (node != NULL)
    {
      tuple = PyTuple_New(2);
      Py_INCREF(KEY(node));
      Py_INCREF(VALUE(node));
      PyTuple_SET_ITEM(tuple, 0, KEY(node));
      PyTuple_SET_ITEM(tuple, 1, VALUE(node));
      return tuple;
    }
  Py_INCREF(Py_None);
  return Py_None;
}

node_t *ct_max_node(node_t *root)
// get node with largest key
{
  if (root == NULL) return NULL;
  while (RIGHT_NODE(root) != NULL)
      root = RIGHT_NODE(root);
  return root;
}

node_t *ct_min_node(node_t *root)
// get node with smallest key
{
  if (root == NULL) return NULL;
  while (LEFT_NODE(root) != NULL)
      root = LEFT_NODE(root);
  return root;
}

int ct_bintree_remove(node_t **rootaddr, PyObject *key, PyObject *cmp)
// attention: rootaddr is the address of the root pointer
{
  node_t *node, *parent, *replacement;
  int direction, cmp_res, down_dir;

  node = *rootaddr;

  if (node == NULL)
    {
      return 0; // root is NULL
    }
  else
    {
      parent = NULL;
      direction = 0;

      while(1)
        {
          cmp_res = ct_compare(cmp, key, KEY(node));
          if (cmp_res == 0) // key found, remove node
            {
              if ((LEFT_NODE(node) != NULL) && (RIGHT_NODE(node) != NULL))
                {
                  // find replacement node: smallest key in right-subtree
                  parent = node;
                  direction = RIGHT;
                  replacement = RIGHT_NODE(node);
                  while (LEFT_NODE(replacement) != NULL)
                    {
                      parent = replacement;
                      direction = LEFT;
                      replacement = LEFT_NODE(replacement);
                    }
                  LINK(parent, direction) = RIGHT_NODE(replacement);
                  // swap places
                  ct_swap_data(node, replacement);
                  node = replacement; // delete replacement node
                }
              else
                {
                  down_dir = (LEFT_NODE(node) == NULL) ? RIGHT : LEFT;
                  if (parent == NULL) // root
                    {
                      *rootaddr = LINK(node, down_dir);
                    }
                  else
                    {
                      LINK(parent, direction) = LINK(node, down_dir);
                    }
                }
              ct_delete_node(node);
              return 1; // remove was success full
            }
          else
            {
              direction = (cmp_res < 0) ? LEFT : RIGHT;
              parent = node;
              node = LINK(node, direction);
              if (node == NULL)
                {
                  return 0; // error key not found
                }
            }
        }
    }
}

int ct_bintree_insert(node_t **rootaddr,  PyObject *key, PyObject *value, PyObject *cmp)
// attention: rootaddr is the address of the root pointer
{
  node_t *parent, *node;
  int direction, cval;
  node = *rootaddr;
  if (node == NULL)
    {
      *rootaddr = ct_new_node(key, value, 0); // new node is also the root
    }
  else
    {
      direction = LEFT;
      parent = NULL;
      while(1)
        {
          if (node == NULL)
            {
              LINK(parent, direction) = ct_new_node(key, value, 0);
              return 1;
            }
          cval = ct_compare(cmp, key, KEY(node));
          if (cval == 0) // key exists, replace value object
            {
              Py_XDECREF(VALUE(node)); // release old value object
              VALUE(node) = value; // set new value object
              Py_INCREF(value); // take new value object
              return 0;
            }
          else
            {
              parent = node;
              direction = (cval < 0) ? LEFT : RIGHT;
              node = LINK(node, direction);
            }
        }
    }
  return 1;
}

static int is_red (node_t *node)
{
  return (node != NULL) && (RED(node) == 1);
}

#define rb_new_node(key, value) ct_new_node(key, value, 1)

static node_t *rb_single(node_t *root, int dir)
{
  node_t *save = root->link[!dir];

  root->link[!dir] = save->link[dir];
  save->link[dir] = root;

  root->red = 1;
  save->red = 0;

  return save;
}

static node_t *rb_double(node_t *root, int dir)
{
  root->link[!dir] = rb_single(root->link[!dir], !dir);

  return rb_single(root, dir);
}

#define rb_new_node(key, value) ct_new_node(key, value, 1)

int avl_insert(node_t **rootaddr, PyObject *key, PyObject *value, PyObject *cmp)
{
  node_t *root = *rootaddr;

  if (root == NULL)
    {
    /*
      We have an empty tree; attach the
      new node directly to the root
    */
      *rootaddr = rb_new_node(key, value);
    }
  else
    {
      node_t head = {0}; /* False tree root */
      node_t *g, *t;     /* Grandparent & parent */
      node_t *p, *q;     /* Iterator & parent */
      int dir = 0, last = 0;

      /* Set up our helpers */
      t = &head;
      g = p = NULL;
      q = t->link[1] = root;

      /* Search down the tree for a place to insert */
      for ( ; ; )
        {
          if ( q == NULL )
            {
              /* Insert a new node at the first null link */
              p->link[dir] = q = rb_new_node(key, value);
              if (q == NULL)
                return 0;
            }
          else if (is_red(q->link[0]) && is_red(q->link[1]))
            {
              /* Simple red violation: color flip */
              q->red = 1;
              q->link[0]->red = 0;
              q->link[1]->red = 0;
            }

          if (is_red(q) && is_red(p))
            {
              /* Hard red violation: rotations necessary */
              int dir2 = t->link[1] == g;

              if (q == p->link[last])
                t->link[dir2] = rb_single ( g, !last );
              else
                t->link[dir2] = rb_double ( g, !last );
            }

          /*
            Stop working if we inserted a node. This
            check also disallows duplicates in the tree
          */
          int cmp_res;
          cmp_res = ct_compare(cmp, KEY(q), key);
          if (cmp_res == 0)
            {
              VALUE(q) = value; // replace existing value
              return 0;
            }
          last = dir;
          dir = cmp_res < 0;

          /* Move the helpers down */
          if (g != NULL)
            t = g;

          g = p, p = q;
          q = q->link[dir];
        }
        /* Update the root (it may be different) */
      *rootaddr = head.link[1];
    }
  /* Make the root black for simplified logic */
  RED(*rootaddr) = 0;
  return 1;
}

int rb_remove(node_t **rootaddr, PyObject *key, PyObject *cmp)
{
  node_t root = *rootaddr;


  if (root != NULL)
    {
      node_t head = {0}; /* False tree root */
      node_t *q, *p, *g; /* Helpers */
      node_t *f = NULL;  /* Found item */
      int dir = 1;

      /* Set up our helpers */
      q = &head;
      g = p = NULL;
      q->link[1] = root;

      /*
        Search and push a red node down
        to fix red violations as we go
      */
      while ( q->link[dir] != NULL )
        {
          int last = dir;
          int cmp_res;

          /* Move the helpers down */
          g = p, p = q;
          q = q->link[dir];

          cmp_res = ct_compare(cmp, q->data, data);
          dir = cmp_res < 0;

          /*
            Save the node with matching data and keep
            going; we'll do removal tasks at the end
          */
          if (cmp_res == 0)
            f = q;

          /* Push the red node down with rotations and color flips */
          if (!is_red(q) && !is_red(q->link[dir]))
            {
              if (is_red(q->link[!dir]))
                p = p->link[last] = rb_single (q, dir);
              else if (!is_red(q->link[!dir]))
                {
                  node_t *s = p->link[!last];

                  if (s != NULL)
                    {
                      if (!is_red(s->link[!last]) && !is_red( s->link[last]))
                        {
                          /* Color flip */
                          RED(p) = 0;
                          RED(s) = 1;
                          RED(q) = 1;
                        }
                      else
                        {
                          int dir2 = g->link[1] == p;

                          if (is_red(s->link[last]))
                            g->link[dir2] = rb_double(p, last);
                          else if (is_red(s->link[!last]))
                            g->link[dir2] = rb_single(p, last);

                          /* Ensure correct coloring */
                          RED(q) = RED(g->link[dir2]) = 1;
                          RED(g->link[dir2]->link[0]) = 0;
                          RED(g->link[dir2]->link[1]) = 0;
                        }
                    }
                }
            }
        }

      /* Replace and remove the saved node */
      if (f != NULL)
        {
          ct_swap_data(f, q);
          p->link[p->link[1] == q] = q->link[q->link[0] == NULL];
          ct_delete_node(q);
        }

      /* Update the root (it may be different) */
      *rootaddr = head.link[1];

      /* Make the root black for simplified logic */
      if (*rootaddr != NULL)
        RED(*rootaddr) = 0;
    }
   return 1;
}
