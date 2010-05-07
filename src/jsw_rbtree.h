#ifndef JSW_RBTREE_H
#define JSW_RBTREE_H

/*
  Red Black balanced tree library

    > Created (Julienne Walker): August 23, 2003
    > Modified (Julienne Walker): March 14, 2008

  This code is in the public domain. Anyone may
  use it or change it in any way that they see
  fit. The author assumes no responsibility for 
  damages incurred through use of the original
  code or any variations thereof.

  It is requested, but not required, that due
  credit is given to the original author and
  anyone who has modified the code through
  a header comment, such as this one.
*/
#ifdef __cplusplus
#include <cstddef>

using std::size_t;

extern "C" {
#else
#include <stddef.h>
#endif

/* Opaque types */
typedef struct jsw_rbtree jsw_rbtree_t;
typedef struct jsw_rbtrav jsw_rbtrav_t;

/* User-defined item handling */
typedef int   (*cmp_f) ( const void *p1, const void *p2 );
typedef void *(*dup_f) ( void *p );
typedef void  (*rel_f) ( void *p );

/* Red Black tree functions */
jsw_rbtree_t *jsw_rbnew ( cmp_f cmp, dup_f dup, rel_f rel );
void          jsw_rbdelete ( jsw_rbtree_t *tree );
void         *jsw_rbfind ( jsw_rbtree_t *tree, void *data );
int           jsw_rbinsert ( jsw_rbtree_t *tree, void *data );
int           jsw_rberase ( jsw_rbtree_t *tree, void *data );
size_t        jsw_rbsize ( jsw_rbtree_t *tree );

/* Traversal functions */
jsw_rbtrav_t *jsw_rbtnew ( void );
void          jsw_rbtdelete ( jsw_rbtrav_t *trav );
void         *jsw_rbtfirst ( jsw_rbtrav_t *trav, jsw_rbtree_t *tree );
void         *jsw_rbtlast ( jsw_rbtrav_t *trav, jsw_rbtree_t *tree );
void         *jsw_rbtnext ( jsw_rbtrav_t *trav );
void         *jsw_rbtprev ( jsw_rbtrav_t *trav );

#ifdef __cplusplus
}
#endif

#endif
