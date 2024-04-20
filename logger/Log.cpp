

#include "Log.h"

namespace Logger {

    static std::unique_ptr<Log> shared_log;

    std::mutex log_mtx;

    void startLog(const std::string_view filepath) {
        shared_log = std::make_unique<Log>(filepath);
        Logger::log(Level::Info, "Initialized log");
    }

    void log(Level l, const std::string_view message) {
        shared_log->addLog(l, message);
    }

    void logFatal(std::string_view message) {
        shared_log->addLog(Logger::Fatal, message);
    }

    void logError(std::string_view message) {
        shared_log->addLog(Logger::Error, message);
    }

    void logWarning(std::string_view message) {
        shared_log->addLog(Logger::Warning, message);
    }

    void logInfo(std::string_view message) {
        shared_log->addLog(Logger::Info, message);
    }

    Log::Log(const std::string_view filepath) : logfile{} {
        logfile.open(filepath);
    }

    void Log::addLog(Logger::Level l, const std::string_view message) {
//        std::lock_guard<std::mutex> guard(log_mtx);
        if(logfile.is_open()) {
            logfile << levels[static_cast<int>(l)] << ": " << message << std::endl;
        }
    }

    Log::~Log() {
        addLog(Level::Info, "Stopped logging.");
        logfile.close();
    }

}