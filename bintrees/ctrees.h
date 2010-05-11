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

typedef node_t* nodeptr;

void ct_delete_node(node_t *node);
void ct_delete_tree(node_t *root);
void ct_swap_data(node_t* node1, node_t* node2);

/* binary tree functions */
int ct_compare(PyObject *compare, PyObject *key1, PyObject *key2);
PyObject *ct_get_item(node_t *root, PyObject *key, PyObject *cmp);
node_t *ct_find_node(node_t *root, PyObject *key, PyObject *cmp);
node_t *ct_succ_node(node_t *root, PyObject *key, PyObject *cmp);
node_t *ct_prev_node(node_t *root, PyObject *key, PyObject *cmp);
node_t *ct_max_node(node_t *root);
node_t *ct_min_node(node_t *root);
int ct_index_of(node_t *root, PyObject *key, PyObject *cmp);
node_t *ct_node_at(node_t *root, int index);

int ct_bintree_insert(node_t **root, PyObject *key, PyObject *value, PyObject *cmp);
int ct_bintree_remove(node_t **root, PyObject *key, PyObject *cmp);

/* avl-tree functions */
int avl_insert(node_t **root, PyObject *key, PyObject *value, PyObject *cmp);
int avl_remove(node_t **root, PyObject *key, PyObject *cmp);

/* rb-tree functions */
int rb_insert(node_t **root, PyObject *key, PyObject *value, PyObject *cmp);
int rb_remove(node_t **root, PyObject *key, PyObject *cmp);

#endif
