#ifndef __NODE_H
#define __NODE_H

#include <Python.h>

typedef struct node node_t;

struct node {
  node_t *link[2];
  PyObject *key;
  PyObject *value;
  int xdata;
};

#define LEFT 0
#define RIGHT 1

#define LEFT_NODE(node) (node->link[LEFT])
#define RIGHT_NODE(node) (node->link[RIGHT])

node_t* node_new(PyObject *key, PyObject *value);
void node_delete(node_t *node);
void tree_clear(node_t *);

#endif