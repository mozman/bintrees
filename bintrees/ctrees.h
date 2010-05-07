#ifndef __NODE_H
#define __NODE_H

#include <Python.h>

typedef struct {
  node_t *link[2];
  PyObject *key;
  PyObject *value;
  int xdata;
} node_t;

#define LEFT 0
#define RIGHT 1
#define KEY(node) (node->key)
#define VALUE(node) (node->value)
#define LEFT_NODE(node) (node->link[LEFT])
#define RIGHT_NODE(node) (node->link[RIGHT])

node_t* node_new(PyObject *key, PyObject *value);
void node_delete(node_t *node);
void tree_clear(node_t *node);
PyObject * node_get_key(node_t *node);
PyObject * node_get_value(node_t *node);
void node_set_value(node_t* node, PyObject *value);
void node_swap_data(node_t* node1, node_t* node2);

#endif