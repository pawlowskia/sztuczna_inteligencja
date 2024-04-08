#include    <iostream>
#include    <vector>
#include    <fstream>
#include    <sstream>
#include    <string>
#include    <map>
#include    <set>
#include    <time.h>
#include    <queue>

using namespace std;

string start_stop = "";
int start_time = 0;
string stop_stop = "";

void read_stops(const string& filename){
    ifstream file(filename);
    if (!file.is_open()){
        cerr << "Error opening file: " << filename << std::endl;
        return;
    }

    getline(file, start_stop);
    getline(file, stop_stop);
    file >> start_time;

    file.close();
}

vector<vector<pair<pair<int, int>, int> > > G; // ((departure time, arrival time), where?)
map<string, int> stops;
map<int, string> spots;
map<int, vector<pair<int,int> > > routes;
map<int, pair<double, double> > coords;
map<pair<int, int>, string> edge_to_line;
priority_queue <pair<int,int>, vector <pair<int, int> >, greater<pair<int, int> > > PQ; // (time, where?)
priority_queue<pair<int, pair<int, int> >, vector<pair<int, pair<int, int> > >, greater<pair<int, pair<int, int> > > > PQ_astar; // (f-value, (time, where?))
priority_queue<pair<pair<int, int>, pair<int, int> >, vector<pair<pair<int, int>, pair<int, int> > >, greater<pair<pair<int, int>, pair<int, int> > > > PQ_astar_lines; // ((f-value, last stop), (time, where?))
vector<bool> vis;
vector<int> arrival_time;

struct entry{
    string id;
    string company;
    string linia;
    int departure_time; // in minutes passed from 00:00
    int arrival_time; // the same
    string start_stop;
    string end_stop;
    string start_stop_lat;
    string start_stop_lon;
    string end_stop_lat;
    string end_stop_lon;
};

vector<entry> entries;

int string_time_to_my_time(string s){
    int t;
    bool bad = false;
    int tmp = 0;
    if (s[0] >= '0' && s[0] <= '9') tmp = tmp * 10 + s[0] - '0';
    else bad = true;
    if (s[1] >= '0' && s[1] <= '9') tmp = tmp * 10 + s[1] - '0';
    else bad = true;
    t = tmp * 60;

    tmp = 0;
    if (s[3] >= '0' && s[3] <= '9') tmp = tmp * 10 + s[3] - '0';
    else bad = true;
    if (s[4] >= '0' && s[4] <= '9') tmp = tmp * 10 + s[4] - '0';
    else bad = true;
    t += tmp;

    if(bad) {
        cerr << "Zle dane!";
        exit(0);
    }

    return t;
}

void read_entries(){
    ifstream file("connection_graph.csv");
    string line;
    bool first_line = true;
    // ,company,linia,departure_time,arrival_time,start_stop,end_stop,start_stop_lat,start_stop_lon,end_stop_lat,end_stop_lon
    // 0,MPK Autobusy,A,20:52:00,20:53:00,Zajezdnia Obornicka,Paprotna,51.14873744,17.02106859,51.14775215,17.02053929
    while(getline(file, line)){
        if (first_line){
            first_line = false;
            continue;
        }
        int params = 11;
        vector<string> values;
        for (int i = 0; i < params; i++){
            values.push_back(line.substr(0, line.find(",")));
            line = line.substr(line.find(",") + 1, line.size());
        }
        // for (int i = 0; i < values.size(); i++){
        //     cout << values[i] << " ";
        // }
        // cout << endl;
        entry e;
        e.id = values[0];
        e.company = values[1];
        e.linia = values[2];
        e.departure_time = string_time_to_my_time(values[3]);
        e.arrival_time = string_time_to_my_time(values[4]);
        e.start_stop = values[5];
        e.end_stop = values[6];
        e.start_stop_lat = values[7];
        e.start_stop_lon = values[8];
        e.end_stop_lat = values[9];
        e.end_stop_lon = values[10];
        entries.push_back(e);
    }
}

void create_graph(){
    // map all nodes
    int counter = 0;
    for (int i = 0; i < entries.size(); i++){
       entry e = entries[i];
        if (stops.find(e.end_stop) == stops.end())
        {
            spots[counter] = e.end_stop;
            coords[counter] = make_pair(stod(e.end_stop_lat), stod(e.end_stop_lon));
            stops[e.end_stop] = counter++;
        }

        if (stops.find(e.start_stop) == stops.end())
        {
            spots[counter] = e.start_stop;
            coords[counter] = make_pair(stod(e.start_stop_lat), stod(e.start_stop_lon));
            stops[e.start_stop] = counter++;
        }
    }

    // create graph
    G.resize(counter + 1);
    for (int i = 0; i < entries.size(); i++){
        entry e = entries[i];
        int start = stops[e.start_stop];
        int end = stops[e.end_stop];
        G[start].push_back(
            make_pair(
                make_pair(
                    e.departure_time,
                    e.arrival_time
                ), 
                end
            )
        );
        edge_to_line[make_pair(start, end)] = e.linia;
    }
    // print first 10 nodes but only first 5 edges
    // for (int i = 0; i < 10; i++){
    //     cout << i << ": ";
    //     for (int j = 0; j < min(5, (int)G[i].size()); j++){
    //         cout << G[i][j].second << "-(" << G[i][j].first.first << ":" << G[i][j].first.second << ")    ";
    //     }
    //     cout << endl;
    // }
    // cout << "number of stops found: " << int(G.size()) << endl;

    //sort all edges in the scope of each stop
    for(int i = 0; i < G.size(); i++)
        sort(G[i].begin(), G[i].end());
}

void cleanup(){
    arrival_time.resize(int(G.size()) + 1);
    vis.resize(int(G.size()) + 1);
    for(int i = 0; i <= G.size(); i++){
        arrival_time[i] = 6000;
        vis[i] = false;
    }
    while(!PQ.empty())
        PQ.pop();
    while(!PQ_astar.empty())
        PQ_astar.pop();
    while(!PQ_astar_lines.empty())
        PQ_astar_lines.pop();
    for(int i = 0; i < G.size(); i++)
        routes[i].clear();
}

void dijkstra(string starting_node, int starting_time){
    cleanup();

    arrival_time[stops[starting_node]] = 0;
    PQ.push(make_pair(starting_time, stops[starting_node]));

    while(!PQ.empty()){
        int current_node = PQ.top().second;
        int current_time = PQ.top().first;
        PQ.pop();

        if(current_node == stops[stop_stop])
            break;

        if(!vis[current_node]){
            vis[current_node] = true;
            
            // consider only connections that are not in the past. thanks to this, we dont have to check for those later.
            vector<pair<pair<int, int>, int> >::iterator it = lower_bound(G[current_node].begin(), G[current_node].end(), make_pair(make_pair(current_time, 0), 0));

            for(; it != G[current_node].end(); ++it){
                pair<pair<int, int>, int> neighbouring_node = *it;   // ((departure time, arrival time), where?)
                int dep_time = neighbouring_node.first.first;
                int arr_time = neighbouring_node.first.second;
                int neighbouring_stop = neighbouring_node.second;
                
                if(!vis[neighbouring_stop]){
                    if(arrival_time[neighbouring_stop] > arr_time){
                        arrival_time[neighbouring_stop] = arr_time;
                        PQ.push(make_pair(arr_time, neighbouring_stop));
                        routes[neighbouring_stop].push_back(make_pair(arr_time, current_node));
                    }
                }
            }
        }
    }
}

double heuristic(int current_node, int destination_node, bool manhattan = false)
{
    double dx = coords[current_node].first - coords[destination_node].first;
    double dy = coords[current_node].second - coords[destination_node].second;
    return sqrt(dx * dx + dy * dy);
}

void A_star(string starting_node, int starting_time, bool manhattan = false){
    cleanup();

    arrival_time[stops[starting_node]] = 0;

    PQ_astar.push(make_pair(0 + heuristic(stops[starting_node], stops[stop_stop], manhattan), make_pair(starting_time, stops[starting_node])));

    while (!PQ_astar.empty())
    {
        int current_node = PQ_astar.top().second.second;
        int current_time = PQ_astar.top().second.first;
        PQ_astar.pop();

        if(current_node == stops[stop_stop])
            break;

        if (!vis[current_node])
        {
            vis[current_node] = true;

            vector<pair<pair<int, int>, int> >::iterator it = lower_bound(G[current_node].begin(), G[current_node].end(), make_pair(make_pair(current_time, 0), 0));

            for (; it != G[current_node].end(); ++it)
            {
                pair<pair<int, int>, int> neighbouring_node = *it;
                int dep_time = neighbouring_node.first.first;
                int arr_time = neighbouring_node.first.second;
                int neighbouring_stop = neighbouring_node.second;

                if(dep_time < current_time)
                    continue;

                if (!vis[neighbouring_stop])
                {
                    if (arrival_time[neighbouring_stop] > arr_time)
                    {
                        arrival_time[neighbouring_stop] = arr_time;
                        PQ_astar.push(make_pair(heuristic(neighbouring_stop, stops[stop_stop], manhattan), make_pair(arr_time, neighbouring_stop)));
                        routes[neighbouring_stop].push_back(make_pair(arr_time, current_node));
                    }
                }
            }
        }
    }
}

void A_star_least_lines_0_1(string starting_node, int starting_time){
    cleanup();

    arrival_time[stops[starting_node]] = 0;

    PQ_astar_lines.push(make_pair(make_pair(0, stops[starting_node]), make_pair(starting_time, stops[starting_node])));

    while (!PQ_astar_lines.empty())
    {
        int current_node = PQ_astar_lines.top().second.second;
        int current_time = PQ_astar_lines.top().second.first;
        int previous_node = PQ_astar_lines.top().first.second;
        PQ_astar_lines.pop();

        if(current_node == stops[stop_stop])
            break;

        if (!vis[current_node])
        {
            vis[current_node] = true;

            vector<pair<pair<int, int>, int> >::iterator it = lower_bound(G[current_node].begin(), G[current_node].end(), make_pair(make_pair(current_time, 0), 0));

            for (; it != G[current_node].end(); ++it)
            {
                pair<pair<int, int>, int> neighbouring_node = *it;
                int dep_time = neighbouring_node.first.first;
                int arr_time = neighbouring_node.first.second;
                int neighbouring_stop = neighbouring_node.second;

                if(dep_time < current_time)
                    continue;

                if (!vis[neighbouring_stop])
                {
                    if (arrival_time[neighbouring_stop] > arr_time)
                    {
                        arrival_time[neighbouring_stop] = arr_time;

                        // if edge is from the same line, we add 0 to the f-value, otherwise 1

                        if(edge_to_line[make_pair(current_node, neighbouring_stop)] == edge_to_line[make_pair(previous_node, current_node)])
                            PQ_astar_lines.push(make_pair(make_pair(0, current_node), make_pair(arr_time, neighbouring_stop)));
                        else
                            PQ_astar_lines.push(make_pair(make_pair(1, current_node), make_pair(arr_time, neighbouring_stop)));

                        routes[neighbouring_stop].push_back(make_pair(arr_time, current_node));
                    }
                }
            }
        }
    }
}

void A_star_least_lines(string starting_node, int starting_time){
    cleanup();

    arrival_time[stops[starting_node]] = 0;

    PQ_astar_lines.push(make_pair(make_pair(0, stops[starting_node]), make_pair(starting_time, stops[starting_node])));

    while (!PQ_astar_lines.empty())
    {
        int current_node = PQ_astar_lines.top().second.second;
        int current_time = PQ_astar_lines.top().second.first;
        int previous_node = PQ_astar_lines.top().first.second;
        PQ_astar_lines.pop();

        if(current_node == stops[stop_stop])
            break;

        if (!vis[current_node])
        {
            vis[current_node] = true;

            vector<pair<pair<int, int>, int> >::iterator it = lower_bound(G[current_node].begin(), G[current_node].end(), make_pair(make_pair(current_time, 0), 0));

            for (; it != G[current_node].end(); ++it)
            {
                pair<pair<int, int>, int> neighbouring_node = *it;
                int dep_time = neighbouring_node.first.first;
                int arr_time = neighbouring_node.first.second;
                int neighbouring_stop = neighbouring_node.second;

                if(dep_time < current_time)
                    continue;

                if (!vis[neighbouring_stop])
                {
                    if (arrival_time[neighbouring_stop] > arr_time)
                    {
                        arrival_time[neighbouring_stop] = arr_time;

                        // if edge is from the same line, we add 0 to the f-value, otherwise 1
                        double penalty = 1.0 / heuristic(neighbouring_stop, stops[stop_stop]);


                        if(edge_to_line[make_pair(current_node, neighbouring_stop)] == edge_to_line[make_pair(previous_node, current_node)])
                            PQ_astar_lines.push(make_pair(make_pair(0 - penalty, current_node), make_pair(arr_time, neighbouring_stop)));
                        else
                            PQ_astar_lines.push(make_pair(make_pair(0 + penalty, current_node), make_pair(arr_time, neighbouring_stop)));

                        routes[neighbouring_stop].push_back(make_pair(arr_time, current_node));
                    }
                }
            }
        }
    }
}

void print_time_from_int(int x) {
    if(x/60 < 10 && x % 60 < 10)
        cout << '0' << x/60 << ":0" << x%60 << ":00";
    else if(x/60 < 10)
        cout << '0' << x/60 << ":" << x%60 << ":00";
    else if(x%60 < 10)
        cout << x/60 << ":0" << x%60 << ":00";
    else 
        cout << x/60 << ":" << x%60 << ":00";
}

void print_route(){
    int first_stop = stops[start_stop];
    int current_stop = stops[stop_stop];
    int current_time = start_time;
    int line_changes = 0;
    string prev_line = "";
    cout << "route " << spots[first_stop] << " at ";
    print_time_from_int(current_time);
    cout << " to destination: " << spots[current_stop] << endl << endl;

    while(current_stop != first_stop) {
        vector<pair<int, int> > v = routes[current_stop];
        if(v.empty()) break;
        current_time = v[v.size() - 1].first;
        cout << spots[current_stop] << " at ";
        print_time_from_int(current_time);
        string line = edge_to_line[make_pair(v[v.size() - 1].second, current_stop)];
        cout << " line " << line << endl;
        if(prev_line != line)
            line_changes++;
        current_stop = v[v.size() - 1].second;
        prev_line = line;
    }
    cout << spots[current_stop] << " at ";
    print_time_from_int(current_time);
    cout << endl;

    cout << "Line changes: " << line_changes << endl << endl;
}

int main(){
    read_stops("stops.txt");
    read_entries();
    create_graph();
    // start counting time
    clock_t start = clock();
    dijkstra(start_stop, start_time);
    // print time
    cout << "Dijkstra time: " << (clock() - start) / (double)(CLOCKS_PER_SEC) << " s" << endl << endl;
    print_route();


    start = clock();
    A_star(start_stop, start_time);
    cout << endl << "A* time: " << (clock() - start) / (double)(CLOCKS_PER_SEC) << " s" << endl;
    print_route();

    start = clock();
    A_star(start_stop, start_time, true);
    cout << endl << "A* time with Manhattan heuristic: " << (clock() - start) / (double)(CLOCKS_PER_SEC) << " s" << endl;
    print_route();

    start = clock();
    A_star_least_lines_0_1(start_stop, start_time);
    cout << endl << "A* time with least lines heuristic 0-1: " << (clock() - start) / (double)(CLOCKS_PER_SEC) << " s" << endl;
    print_route();

    start = clock();
    A_star_least_lines(start_stop, start_time);
    cout << endl << "A* time with least lines heuristic: " << (clock() - start) / (double)(CLOCKS_PER_SEC) << " s" << endl;
    print_route();

    return 0;
}