#ifndef __CTREES_H
#define __CTREES_H

#include <Python.h>

typedef struct tree_node node_t;

struct tree_node {
  node_t *link[2];
  PyObject *key;
  PyObject *value;
  int xdata;
};

node_t *ct_new_node(PyObject *key, PyObject *value, int xdata);
void ct_delete_node(node_t *node);
void ct_delete_tree(node_t *root);
PyObject *ct_get_key(node_t *node);
PyObject *ct_get_value(node_t *node);
void ct_set_value(node_t* node, PyObject *value);
void ct_swap_data(node_t* node1, node_t* node2);

/* binary tree functions */
node_t *ct_find_node(node_t *root, PyObject *key, PyObject *cmp);
int ct_bintree_insert(node_t **root, PyObject *key, PyObject *value, PyObject *cmp);
int ct_bintree_remove(node_t **root, PyObject *key, PyObject *cmp);

/* avl-tree functions */
int ct_avltree_insert(node_t **root, PyObject *key, PyObject *value, PyObject *cmp);
int ct_avltree_remove(node_t **root, PyObject *key, PyObject *cmp);

/* rb-tree functions */
int ct_rbtree_insert(node_t **root, PyObject *key, PyObject *value, PyObject *cmp);
int ct_rbtree_remove(node_t **root, PyObject *key, PyObject *cmp);

#endif
