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

    CROW_ROUTE(app,"/postTest").methods(crow::HTTPMethod::POST)([](const crow::request& req){
        auto reqBod = crow::json::load(req.body);
        if (!reqBod) {
            return crow::response(400, "Invalid JSON");
        }
        // std::string string = reqBod["test"].s();
        crow::json::wvalue sendS(reqBod);
        // sendS["data"]=string;
        return (crow::response) sendS;
    });

    app.port(18080).multithreaded().run();
}