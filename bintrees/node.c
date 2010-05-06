#include "node.h"
#include <Python.h>

#define LEFT 0
#define RIGHT 1

node_t * node_new(PyObject *key, PyObject *value)
{
    node_t * new_node = PyMem_Malloc(sizeof(*new_node))
    if new_node != NULL) {
        new_node->key = key;
        Py_INCREF(key);
        new_node->value = value;
        Py_INCREF(value)
        new_node->link[LEFT] = NULL;
        new_node->link[RIGHT] = NULL;
        new_node->xdata = 0;
    }
    return new_node
}

void node_delete(node_t *node)
{
    Py_XDECREF(node->key);
    Py_XDECREF(node->value);
    PyMem_Free(node);
}

void tree_clear(node_t * node)
{
    if LEFT_NODE(node) != NULL {
        tree_clear(LEFT_NODE(node))
    if RIGHT_NODE(node) != NULL {
        tree_clear(RIGHT_NODE(node)
    node_delete(node)
}