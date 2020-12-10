#include <vector>
#include <iomanip>
#include <iostream>
using namespace std;
class NetPage;
template <typename T>
struct NetPageIndex{
    T index;
    NetPageIndex<T>* pred;
    NetPageIndex<T>* succ;
    NetPageIndex(){ pred = NULL; succ = NULL; }
    NetPageIndex(T i, NetPageIndex<T>* p=NULL, NetPageIndex<T>* s=NULL):index(i),pred(p),succ(s){}
    void insertSucc(T const& a){
        NetPageIndex<T>* x = new NetPageIndex(a, succ);
        succ->pred = x; succ = x;
    }
    void insertPred(T const& a){
        NetPageIndex<T>* x = new NetPageIndex(a, pred, this);
        pred->succ = x; pred = x;
    }
};


template <typename T> class NetPageList{
public:
    int size;
    NetPageIndex<T>* header;
    NetPageIndex<T>* trailer;
    NetPageIndex<T>* cursor;
    NetPageList(){
        header = new NetPageIndex<T>(-1);
        trailer = new NetPageIndex<T>(-1);
        header->succ = trailer;
        trailer->pred = header;
        size = 0;
    }
    void insert(T const& e){
        size++;
        trailer->insertPred(e);
    }
    void initCursor(){
        cursor = header->succ;
    }
    int get(){
        int e = cursor->index;
        cursor = cursor->succ;
        return e;
    }
    NetPageIndex<T>* search(int o){
        initCursor();
        for(int i=0;i<size;i++){
            if(get()==o)break;
        }
        return cursor->pred;
    }
    T remove(NetPageIndex<T>* p){
        size--;
        T e = p->index;
        p->pred->succ = p->succ;
        p->succ->pred = p->pred;
        delete p;
        return e; 
    }
};
class NetPage{
public:
    int index;
    double probability;
    double probability1;
    bool scc;
    NetPageList<int>* out;
    NetPageList<int>* in;
    vector<int>* sccOut;
    vector<int>* sccIn;
    NetPage(){
        out = new NetPageList<int>();
        in = new NetPageList<int>();
        scc = true;
        sccOut = NULL;
        sccIn = NULL;
    }
    NetPage(int index):index(index){
        out = new NetPageList<int>();
        in = new NetPageList<int>();
        scc = true;
        sccOut = NULL;
        sccIn = NULL;
    }
    void constructSccOut(){
        if(sccOut!=NULL){
            delete sccOut;
        }
        sccOut = new vector<int>(out->size);
        out->initCursor();
        for(int i=0;i<out->size;i++){
            sccOut->at(i) = out->get();
        }
        if(sccIn!=NULL){
            delete sccIn;
        }
        sccIn = new vector<int>(in->size);
        in->initCursor();
        for(int i=0;i<in->size;i++){
            sccIn->at(i) = in->get();
        }
    }
    void init(int i){
        index = i;
    }
    void addOut(int o){
        out->insert(o);
    }
    void addIn(int i){
        in->insert(i);
    }
    int removeOut(int o){
        NetPageIndex<int>* p = out->search(o);
        int e = out->remove(p);
        return e;
    }
    int removeIn(int i){
        NetPageIndex<int>* p = in->search(i);
        int e = in->remove(p);
        return e;
    }
    void print(){
        if(scc){
            cout<<"scc nodes";
        }
        out->initCursor();
        cout<<index<<"size"<<out->size<<" ";
        cout<<index<<"->";
        for(int i=0;i<out->size;i++){    
            cout<<out->get();
        }
        in->initCursor();
        cout<<index<<"<-";
        for(int i=0;i<in->size;i++){    
            cout<<in->get();
        }
        cout<<endl;
    }
};
class NetGraph{
public:
    int nodes;
    int edges;
    vector<NetPage>* pages;
    vector<NetPage*>* scc;
    NetGraph(int n, int m):nodes(n),edges(m){
        pages = new vector<NetPage>(n);
        scc = new vector<NetPage*>(0);
        for(int i=0;i<n;i++){
            pages->at(i).init(i);
        }
    }
    int appendEdge(int src, int dest){
        pages->at(src).addOut(dest);
        pages->at(dest).addIn(src);
        return 1;
    }
    int removeDeadEnd(){
        int deadEnd = 1;
        int inC = 1;
        while(deadEnd!=0|inC!=0){
            deadEnd = 0;
            inC = 0;
            for(int i=0;i<nodes;i++){
                if(pages->at(i).scc){
                    if(pages->at(i).out->size==0){
                        deadEnd++;
                        pages->at(i).in->initCursor();
                        for(int j=0;j<pages->at(i).in->size;j++){
                            int temp = pages->at(i).in->get();
                            if(pages->at(temp).scc)
                                pages->at(temp).removeOut(i);
                        }
                        pages->at(i).scc = false;
                    }else if(pages->at(i).in->size==0){
                        inC++;
                        pages->at(i).out->initCursor();
                        for(int j=0;j<pages->at(i).out->size;j++){
                            int temp = pages->at(i).out->get();
                            if(pages->at(temp).scc)
                                pages->at(temp).removeIn(i);
                        }
                        pages->at(i).scc = false;
                    }
                }
            }
        }
        return deadEnd;
    }
    
    void printGraph(){
        for(int i=0;i<nodes;i++){
            pages->at(i).print();
        }
    }
    int constructScc(){
        for(int i=0;i<nodes;i++){
            if(pages->at(i).scc){
                scc->push_back(&(pages->at(i)));
                pages->at(i).constructSccOut();
            }
        }
        return scc->size();
    }
    double matrixDot(){
        double maxEpsilon=0;
        for(int i=0;i<scc->size();i++){
            for(int j=0;j<scc->at(i)->in->size;j++){
                scc->at(i)->probability1 += pages->at(scc->at(i)->sccIn->at(j)).probability/pages->at(scc->at(i)->sccIn->at(j)).out->size;
            }
        }
        for(int i=0;i<scc->size();i++){
            if((scc->at(i)->probability = scc->at(i)->probability1)>maxEpsilon)
                maxEpsilon = scc->at(i)->probability = scc->at(i)->probability1;
            scc->at(i)->probability = scc->at(i)->probability1;
            scc->at(i)->probability1 = 0;
            //cout<<scc->at(i)->index<<"is"<<scc->at(i)->probability<<endl;
        }
        return maxEpsilon;
    }
    void initSccProbability(){
        // init probability
        for(int i=0;i<scc->size();i++){
            scc->at(i)->probability = 1.0/scc->size();
            scc->at(i)->probability1 = 0;
        }
    }
    int pagerank(double epsilon=0.0000001){
        double maxEpsilon = matrixDot();;
        int times =0;
        while(maxEpsilon>epsilon&times<100){
            maxEpsilon = matrixDot();
            times++;
        }
        return 1;
    }
    double getRank(int node){
        if(pages->at(node).scc)return pages->at(node).probability;
        else
            return -1;
    }
};
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
    //net.printGraph();
    net.removeDeadEnd();
    //net.printGraph();
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