#include "crow_all.h"
#include <cpr/cpr.h>
#include <nlohmann/json.hpp>

using Json = nlohmann::json;


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

    CROW_ROUTE(app,"/ai").methods(crow::HTTPMethod::POST)([](const crow::request& req){
        auto reqBod = crow::json::load(req.body);
        if (!reqBod) {
            return crow::response(400, "Invalid JSON");
        }

        std::string userInput = reqBod["userInput"].s();

        Json aiSend = Json::object( {
            {"contents", Json::array{
                Json::object{
                    {"role", "user"},
                    {"parts", Json::array{
                        Json::object{
                            {"text", userInput}
                        }
                    }}
                }
            }},
            {"generationConfig", Json::object{
                {"responseMimeType", "text/plain"}
            }}
        });

        cpr::Response aiResp = cpr::Post(
            cpr::Url{"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:GenerateContent?key=${AI_KEY}"},
            cpr::Header{{"Content-Type", "application/json"}},
            cpr::Body{aiSend.dump()}
        );
        
        return crow::response(aiResp.text);
    });

    app.port(18080).multithreaded().run();
}