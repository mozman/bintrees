#include "ctrees.h"
#include "stack.h"

node_stack_t *stack_init(int size)
{
  node_stack_t *stack;

  stack = PyMem_Malloc(sizeof(node_stack_t));
  stack->stack = PyMem_Malloc(sizeof(node_t *) * size);
  stack->size = size;
  stack->stackptr = 0;
  return stack;
}

void stack_delete(node_stack_t *stack)
{
  PyMem_Free(stack->stack);
  PyMem_Free(stack);
}

void stack_push(node_stack_t *stack, node_t *node)
{
  stack->stack[stack->stackptr++] = node;
  if (stack->stackptr > stack->size)
    {
      stack->size *= 2;
      stack->stack = PyMem_Realloc(stack->stack, sizeof(node_t *) * stack->size);
    }
}

node_t *stack_pop(node_stack_t *stack)
{
  return stack->stack[stack->stackptr--];
}

int stack_is_empty(node_stack_t *stack)
{
  return (stack->stackptr == 0);
}

void stack_reset(node_stack_t *stack)
{
  stack->stackptr = 0;
}
