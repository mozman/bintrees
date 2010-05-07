#include "node.h"
#include <Python.h>

node_t * node_new(PyObject *key, PyObject *value)
{
    node_t * new_node = PyMem_Malloc(sizeof(*new_node));
    if (new_node != NULL)
        {
            KEY(new_node) = key;
            Py_INCREF(key);
            VALUE(new_node) = value;
            Py_INCREF(value);
            LEFT_NODE(new_node) = NULL;
            RIGHT_NODE(new_node) = NULL;
            new_node->xdata = 0;
        }
    return new_node;
}

void node_delete(node_t *node)
{
    Py_XDECREF(KEY(node));
    Py_XDECREF(VALUE(node));
    PyMem_Free(node);
}

void tree_clear(node_t * node)
{
    if (LEFT_NODE(node) != NULL)
        {
            tree_clear(LEFT_NODE(node));
        };
    if (RIGHT_NODE(node) != NULL)
        {
            tree_clear(RIGHT_NODE(node));
        };
    node_delete(node);
}

PyObject *node_get_value(node_t *node)
{
    Py_INCREF(NODE_KEY(node))
    return NODE_KEY(node)
}

void node_set_value(node_t *node, PyObject *value)
{
    Py_INCREF(value)
    NODE_VALUE(node) = value
}

PyObject *node_get_key(node_t *node)
{
    Py_INCREF(NODE_VALUE(node))
    return NODE_VALUE(node)
}

void node_swap_data(node_t* node1, node_t* node2)
{
    PyObject *tmp
    tmp = NODE_KEY(node1);
    NODE_KEY(node1) = NODE_KEY(node2);
    NODE_KEY(node2) = tmp
    tmp = NODE_VALUE(node1);
    NODE_VALUE(node1) = NODE_VALUE(node2);
    NODE_VALUE(node2) = tmp
}