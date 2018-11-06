#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <fcntl.h>
#include <unistd.h>
#include <dirent.h>
#define N 9570


struct queue {
    int items[N];
    int front;
    int rear;
};

struct queue* createQueue();
void enqueue(struct queue* q, int);
int dequeue(struct queue* q);
void display(struct queue* q);
int isEmpty(struct queue* q);
void printQueue(struct queue* q);

struct node
{
    int vertex;
    struct node* next;
};

struct node* createNode(int);

struct Graph
{
    int numVertices;
    struct node** adjLists;
    int* visited;
};

struct Graph* createGraph(int vertices);
void addEdge(struct Graph* graph, int src, int dest);
void printGraph(struct Graph* graph);
void bfs(struct Graph* graph, int startVertex, int** dist, int nodes);

int main()
{

    int**dist = (int**)malloc(sizeof(int*)*N);
    for (int i=0;i<N;i++)
	dist[i] = (int*)malloc(sizeof(int)*N);
    for (int i=0;i<N;i++)
	for (int j=0; j<N;j++)
		dist[i][j]=0;
    struct Graph* graph = createGraph(N);
    FILE* edges;
    FILE* distances;
    edges=fopen("../PPIN_Construction/EdgeLists_Relabeled/Arabidopsis_thaliana_Columbia.edgelist","r");
    distances=fopen("DistMats/Arabidopsis_thaliana_Columbia-Distances.txt","w");
    char line[12];
    while(fgets(line, 100, edges)) 
    {
        int n1=0, n2=0,i=0;
        while (isdigit(line[i]))
        {	
	    n1=n1*10+(line[i]-'0');
            i++;
        }
	i++;
        while (isdigit(line[i]))
        {	
	    n2=n2*10+(line[i]-'0');
            i++;
        }
	addEdge(graph,n1,n2);
    }
    fclose(edges);
    for (int i=0;i<N;i++)
	bfs(graph, i, dist,N);
    for (int i=0;i<N;i++)
    {
	for (int j=0; j<N;j++)
		fprintf(distances,"%d ",dist[i][j]);
	fprintf(distances, "\n");
    }
    fclose(distances);
    return 0;
}

void bfs(struct Graph* graph, int startVertex, int** dist, int nodes) {

    struct queue* q = createQueue();
    struct Graph* replica = createGraph(nodes);
    replica->visited[startVertex] = 1;
    enqueue(q, startVertex);
    
    while(!isEmpty(q)){
        int currentVertex = dequeue(q);
    
       struct node* temp = graph->adjLists[currentVertex];
    
       while(temp) {
            int adjVertex = temp->vertex;

            if(replica->visited[adjVertex] == 0){
                replica->visited[adjVertex] = 1;
		if (dist[startVertex][adjVertex]==0)
			dist[startVertex][adjVertex]=dist[startVertex][currentVertex]+1;
                enqueue(q, adjVertex);
		
            }
            temp = temp->next;
       }
    }
}

 
struct node* createNode(int v)
{
    struct node* newNode = malloc(sizeof(struct node));
    newNode->vertex = v;
    newNode->next = NULL;
    return newNode;
}
 

struct Graph* createGraph(int vertices)
{
    struct Graph* graph = malloc(sizeof(struct Graph));
    graph->numVertices = vertices;
 
    graph->adjLists = malloc(vertices * sizeof(struct node*));
    graph->visited = malloc(vertices * sizeof(int));
    
 
    int i;
    for (i = 0; i < vertices; i++) {
        graph->adjLists[i] = NULL;
        graph->visited[i] = 0;
    }
 
    return graph;
}
 
void addEdge(struct Graph* graph, int src, int dest)
{
    // Add edge from src to dest
    struct node* newNode = createNode(dest);
    newNode->next = graph->adjLists[src];
    graph->adjLists[src] = newNode;
 
    // Add edge from dest to src
    newNode = createNode(src);
    newNode->next = graph->adjLists[dest];
    graph->adjLists[dest] = newNode;
}

struct queue* createQueue() {
    struct queue* q = malloc(sizeof(struct queue));
    q->front = -1;
    q->rear = -1;
    return q;
}


int isEmpty(struct queue* q) {
    if(q->rear == -1) 
        return 1;
    else 
        return 0;
}

void enqueue(struct queue* q, int value){
    if(q->rear != N-1)
   {
        if(q->front == -1)
            q->front = 0;
        q->rear++;
        q->items[q->rear] = value;
    }
}

int dequeue(struct queue* q){
    int item;
    if(isEmpty(q)){
        item = -1;
    }
    else{
        item = q->items[q->front];
        q->front++;
        if(q->front > q->rear){
            q->front = q->rear = -1;
        }
    }
    return item;
}

void printQueue(struct queue *q) {
    int i = q->front;

    if(!isEmpty(q)) {
        for(i = q->front; i < q->rear + 1; i++) {
                printf("%d ", q->items[i]);
        }
    }    
}
