#include "crow_all.h"
#include <cpr/cpr.h>


int main (){
    crow::SimpleApp app;

    CROW_ROUTE(app,"/")([](){
        return "hello world";
    });

    CROW_ROUTE(app,"/getTest")([](){
        cpr::Response r = cpr::Get(cpr::Url{"https://google.com"});
        return r.text;
    });

    app.port(18080).multithreaded().run();
}