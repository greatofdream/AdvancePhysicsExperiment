#include <iostream>
#include <iomanip>
#include "pagerank.h"
using namespace std;
int main(){
    int n=0, m=0;// node, edge number
    int src, dest;
    scanf("%d %d",&n,&m);
    //cout<<"n:"<<n<<"m"<<m<<endl;

    NetGraph net(n,m);
    for(int i=0;i<m;i++){
        scanf("%d %d",&src,&dest);
        net.appendEdge(src,dest);
    }
    net.printGraph();
    net.removeDeadEnd();
    net.printGraph();
    net.constructScc();
    net.initSccProbability();
    net.pagerank();

    int k;
    scanf("%d",&k);// output the edge
    int* nodeList = new int[k];
    for(int i=0;i<k;i++){
        scanf("%d",&nodeList[i]);
    }
    double rank = 0;
    for(int i=0;i<k;i++){
        rank = net.getRank(nodeList[i]);
        if(rank<0){cout<<"None"<<endl;}
        else{cout<<setiosflags(ios::fixed)<<setprecision(5)<<rank<<endl;}
    }
    return 0;
}