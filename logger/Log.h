//
// Created by Geoff Twardokus on 2/17/24.
//

#ifndef V2VERIFIER_LOG_H
#define V2VERIFIER_LOG_H

#include <fstream>
#include <mutex>
#include <string>

namespace Logger {

    enum Level {
        Fatal,
        Error,
        Warning,
        Info
    };

    void startLog(std::string_view filepath);
    void log(Level l, std::string_view message);
    void logFatal(std::string_view message);
    void logError(std::string_view message);
    void logWarning(std::string_view message);
    void logInfo(std::string_view message);

    class Log {
    public:
        Log(std::string_view filepath);

        void addLog(Level l, std::string_view message);

        ~Log();

    private:
        std::ofstream logfile;
        std::string levels[4] = {"Fatal", "Error", "Warning", "Info"};
    };



};


#endif //V2VERIFIER_LOG_H
