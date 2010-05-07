#include "ctrees.h"
#include <Python.h>

node_t * ct_new_node(PyObject *key, PyObject *value, int xdata)
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
            XDATA(new_node) = xdata;
        }
    return new_node;
}

void ct_delete_node(node_t *node)
{
    Py_XDECREF(KEY(node));
    Py_XDECREF(VALUE(node));
    PyMem_Free(node);
}

void ct_delete_tree(node_t * root)
{
    if (LEFT_NODE(root) != NULL)
        {
            ct_delete_tree(LEFT_NODE(root));
        };
    if (RIGHT_NODE(root) != NULL)
        {
            ct_delete_tree(RIGHT_NODE(root));
        };
    ct_delete_node(root);
}

PyObject *ct_get_value(node_t *node)
{
    /* Py_INCREF(NODE_KEY(node)) is this ok? */
    return KEY(node);
}

void node_set_value(node_t *node, PyObject *value)
{
    Py_INCREF(value);
    VALUE(node) = value;
}

PyObject *ct_get_key(node_t *node)
{
    /* Py_INCREF(NODE_VALUE(node)) is this ok? */
    return VALUE(node);
}

void ct_swap_data(node_t* node1, node_t* node2)
{
    PyObject *tmp;
    tmp = KEY(node1);
    KEY(node1) = KEY(node2);
    KEY(node2) = tmp;
    tmp = VALUE(node1);
    VALUE(node1) = VALUE(node2);
    VALUE(node2) = tmp;
}

node_t *ct_find_node(node_t *root, PyObject *key, PyObject *cmp)
{
    return NULL;
}

node_t *ct_bintree_remove(node_t *root, PyObject *key, PyObject *cmp)
{
    return root;
}

node_t *ct_bintree_insert(node_t *root, PyObject *key, PyObject *value, PyObject *cmp)
{
    return root;
}
