
#include<stdio.h>
#include<stdlib.h>
#include<ctype.h>

void hexdump(void *mem, unsigned int len)
{
  unsigned int i, j;

  for(i = 0; i < len + ((len % 16) ? (16 - len % 16) : 0); i++)
  {
    /* print offset */
    if(i % 16 == 0)
    {
      printf("0x%04x: ", i);
    }

    /* print hex data */
    if(i < len)
    {
      printf("%02x ", 0xFF & ((char*)mem)[i]);
    }
    else /* end of block, just aligning for ASCII dump */
    {
      printf("   ");
    }

    /* print ASCII dump */
    if(i % 16 == (16 - 1))
    {
      for(j = i - (16 - 1); j <= i; j++)
      {
        if(j >= len) /* end of block, not really printing */
        {
          putchar(' ');
        }
        else if(isprint((((char*)mem)[j] & 0x7F))) /* printable char */
        {
          putchar(0xFF & ((char*)mem)[j]);
        }
        else /* other char */
        {
          putchar('.');
        }
      }
      putchar('\n');
    }
  }
}
