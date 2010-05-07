#include "ctrees.h"

typedef struct node_stack node_stack_t;

struct node_stack {
  int stackptr;
  int size;
  node_t *stack;
};

node_stack_t *stack_init(int size)
{
  stack = PyMem_Malloc(sizeof(node_stack_t));
  stack->stack = PyMem_Malloc(sizeof(node_t)*size);
  stack->size = size;
  stack->stackptr = 0;
  return stack
}

void stack_delete(node_stack_t *stack)
{
  PyMem_Free(stack->stack);
  PyMem_Free(stack);
}

void stack_push(node_stack_t *stack, node_t *node)
{
  stack->stack[stack->stackptr++] = node
  if (stack->stackptr > stack->size)
    {
      //realloc
    }
}

node_t *stack_pop(node_stack_t *stack)
{
  return stack->stack[stack->stackptr--]
}
