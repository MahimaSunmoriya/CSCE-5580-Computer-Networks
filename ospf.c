#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define MAX_NODES 100       /* maximum number of nodes */
#define INFINITY 99999999   /* constant for infinity value */
#define UNDEFINED -1        /* undefined node index */


/** struct for a node in the network */
typedef struct node{
	int u;          /* vertex number */
	int distance;   /* distance from source vertex */
	int parent;     /* parent in the shortest path */
} Node;


typedef struct min_queue{
	Node* nodes[MAX_NODES];
	int numNodes;
} MinQueue;

/*
 * Add a node into a min queue
 * Arguments:
 *   q    - a min queue where priority is based on minimum distance of node
            from source node
 *   n    - new node to be added
 */
void queueAdd(MinQueue *q, Node *n);

/*
 * Extract and remove the min node from the queue
 * Arguments:
 *   q  - the min queue
 # Return the min node from the queue
 */
Node* queueExtractMin(MinQueue *q);

/* Check whether a min queue is empty or not 
   Return 1 if empty, else return 0
*/
int isQueueEmpty(MinQueue *q);

/*
 * Rearrange the queue to maintain its min heap property
 */
void queueMinUpdate(MinQueue *q);

/* Change the distance of a node in the queue */
Node* queueUpdatePriority(MinQueue *q, int u, int distance);

int queueContains(MinQueue *q, int u);

/*
 * This function implements the OSPF link state protocol using the shortest path
 * algorithm on a given network and source node.
 * Arguments:
 *   network    - input network as 2d matrix
 *   firstRouter - the first router
 *   srcRouter   - the source router
 *  numRouters  - number of routers in the network
 */
void shortestPath(int network[MAX_NODES][MAX_NODES], int numRouters, char firstRouter, char srcRouter);


/*
 * Read input network matrix from a file.
 * Arguments:
 *   network   - 2d matrix where network will be saved
 *   filename  - name of input file
 *   numRouters - number of input routers
 */
void readNetworkFromFile(char* filename, int network[MAX_NODES][MAX_NODES], int numRouters);


/* Generate the shortest path as a string from source to target using parent information */
char* createShortestPath(int p[MAX_NODES], int src, int target, char firstNode);

int main()
{
	int numRouters;       /* number of input nodes */
	char firstNode;     /* character of first node */
	char filename[20];  /* input filename of cost matrix */
	char srcRouter;     /* input source router */
	int network[MAX_NODES][MAX_NODES];  /* input network matrix */


	// prompt and read all simulation parameters from user
	printf("OSPF Link-State (LS) Routing:\n");
	printf("-----------------------------\n");
	printf("Enter the number of routers: ");
	scanf("%d", &numRouters);
	getchar();

	printf("Enter filename with cost matrix values: ");
	scanf("%[^\n]s", filename);
	getchar();

	// read the network file, exit on error
	readNetworkFromFile(filename, network, numRouters);

	printf("Enter character representation of first node: ");
	scanf("%c", &firstNode);
	getchar();
	printf("Enter the source router: ");
	scanf("%c", &srcRouter);

	// run OSPF link state protocol
	shortestPath(network, numRouters, firstNode, srcRouter);


	return 0;
}


void queueAdd(MinQueue *q, Node *n)
{
	// add the new node into the queue
	q->nodes[q->numNodes] = n;
	q->numNodes++;
	// rearrange the queue so that min node is at front
	queueMinUpdate(q);
}

int isQueueEmpty(MinQueue *q)
{
	return (q->numNodes == 0);
}

Node* queueExtractMin(MinQueue *q)
{
	Node *minNode = q->nodes[0];
	int size = q->numNodes;
	q->nodes[0] = q->nodes[size - 1];
	(q->numNodes)--;
	return minNode;
}

int queueContains(MinQueue *q, int u)
{
	int size = q->numNodes;
	int i;
	for(i = 0; i < size; i++)
	{
		if(q->nodes[i]->u == u)
			return 1;
	}
	return 0;
}

void queueMinUpdate(MinQueue *q)
{
	int size = q->numNodes;
	int i;
	for(i = (size-1); i >= 1; i--)
	{
		if(q->nodes[i]->distance < q->nodes[i-1]->distance)
		{
			Node *tmp = q->nodes[i];
			q->nodes[i] = q->nodes[i-1];
			q->nodes[i-1] = tmp;
		}
	}
}

Node* queueUpdatePriority(MinQueue *q, int u, int distance)
{
	int size = q->numNodes;
	int i;
	for(i = 0; i < size; i++)
	{
		Node *node = q->nodes[i];
		if(node->u == u)
		{
			node->distance = distance;
			break;
		}
	}
	queueMinUpdate(q);
}


void shortestPath(int network[MAX_NODES][MAX_NODES], int numRouters, char firstRouter, char srcRouter)
{
	int d[MAX_NODES];        // array to store distance of all nodes from start router
	int p[MAX_NODES];        // parent information
	int i;
	int start, u, v;
	MinQueue *q = (MinQueue*)malloc(sizeof(MinQueue));  // min queue
	char vLabel; 
	int path[MAX_NODES];
	int pathLen;
	int parent;
	char *minPathStr;
	int visited[MAX_NODES];


	// get the index of source router
	start = (srcRouter - firstRouter);

	// initialize the distance and parent array
	// add all nodes into the min queue
	for(i = 0; i < numRouters; i++)
	{
		visited[i] = 0;
		d[i] = INFINITY;
		p[i] = UNDEFINED;
		//Node *node = (Node*)malloc(sizeof(Node));
		//node->u = i;
		// if(i != start)
		// 	//node->distance = d[i];
		// {
		// 	//node->distance = 0;
		// 	d[i] = 0;
		// }
		//queueAdd(q, node);
	}
	d[start] = 0;
	Node *node = (Node*)malloc(sizeof(Node));
	node->u = start;
	node->distance = 0;
	node->parent = UNDEFINED;
	queueAdd(q,node);

	// process queue until its empty
	while(!isQueueEmpty(q))
	{
		// extract min node from queue
		Node* node = queueExtractMin(q);
		// u is min node vertex index
		u = node->u;
		visited[u] = 1;
		// iterate over all the neighbors of u in network matrix
		for(v = 0; v < numRouters; v++)
		{
			if(network[u][v] >= 0)
			{
				int altDistance = d[u]+ network[u][v];
				if(altDistance < d[v])
				{
					d[v] = altDistance;
					p[v] = u;
					//queueUpdatePriority(q, v, altDistance);
					if(!queueContains(q,v))
					{
						Node *node = (Node*)malloc(sizeof(Node));
						node->u = v;
						node->distance = altDistance;
						node->parent = u;
						queueAdd(q,node);
					}
				}
			}
		}
	}
	// display shortest path to all nodes from source node
	for(v = 0; v < numRouters; v++)
	{
		vLabel = firstRouter + v;
		minPathStr = createShortestPath(p, start, v, firstRouter);
		printf("%c ==> %c\n", srcRouter, vLabel);
		printf("path cost: %d\n", d[v]);
		printf("path taken: %s\n",minPathStr );
	}

}


void readNetworkFromFile(char* filename, int network[MAX_NODES][MAX_NODES], int numRouters)
{
	int u, v;
	int weight;
	FILE *fin = fopen(filename, "r");

	if(fin == NULL)
	{
		printf("error: could not find file %s!\n", filename);
		exit(0);
	}

	for(u = 0; u < numRouters; u++)
	{
		for(v = 0; v < numRouters; v++)
		{
			fscanf(fin, "%d", &weight);
			network[u][v] = weight;
		}
	}
	fclose(fin);
}

char* createShortestPath(int p[MAX_NODES], int src, int target, char firstNode)
{
	int pathReverse[MAX_NODES];
	int parent;
	int pathLen = 0;
	char *pathStr = (char*)malloc(sizeof(char) * 256);
	char tmp[10];
	char vLabel;
	int i;

	pathReverse[pathLen++] = target;
	parent = p[target];
	while(parent != UNDEFINED)
	{
		pathReverse[pathLen++] = parent;
		parent = p[parent];
	}	
	pathStr[0] = '\0';
	for(i = pathLen-1; i >= 0; i--)
	{
		vLabel = firstNode + pathReverse[i];
		if(i > 0)
			sprintf(tmp, "%c --> ", vLabel);
		else
			sprintf(tmp, "%c", vLabel);
		strcat(pathStr, tmp);
	}

	return pathStr;
}
