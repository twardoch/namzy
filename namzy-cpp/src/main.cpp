// this_file: namzy-cpp/src/main.cpp
#include "namzy.h"

#include <QCoreApplication>
#include <QCommandLineParser>
#include <QTextStream>
#include <QDateTime>

int main(int argc, char* argv[])
{
    QCoreApplication app(argc, argv);
    app.setApplicationName(QStringLiteral("namzy"));
    app.setApplicationVersion(QStringLiteral("1.0.0"));

    QCommandLineParser parser;
    parser.setApplicationDescription(QStringLiteral("Generate fun human-friendly project names."));
    parser.addHelpOption();
    parser.addVersionOption();

    QCommandLineOption countOpt(
        QStringLiteral("count"),
        QStringLiteral("Number of names to generate (default: 1)."),
        QStringLiteral("N"),
        QStringLiteral("1"));
    parser.addOption(countOpt);

    QCommandLineOption seedOpt(
        QStringLiteral("seed"),
        QStringLiteral("RNG seed (default: current timestamp)."),
        QStringLiteral("N"));
    parser.addOption(seedOpt);

    parser.process(app);

    quint64 seed = static_cast<quint64>(QDateTime::currentMSecsSinceEpoch());
    if (parser.isSet(seedOpt)) {
        bool ok = false;
        quint64 v = parser.value(seedOpt).toULongLong(&ok);
        if (!ok) {
            QTextStream(stderr) << "Invalid seed value.\n";
            return 1;
        }
        seed = v;
    }

    bool countOk = false;
    int count = parser.value(countOpt).toInt(&countOk);
    if (!countOk || count < 1) {
        QTextStream(stderr) << "Invalid count value.\n";
        return 1;
    }

    QTextStream out(stdout);
    for (int i = 0; i < count; ++i) {
        Namzy namzy(seed + static_cast<quint64>(i));
        QString name = namzy.generate();
        out << name << "\n";
    }

    return 0;
}
