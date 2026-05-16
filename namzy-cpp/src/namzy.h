// this_file: namzy-cpp/src/namzy.h
#pragma once

#include <QString>
#include <QRandomGenerator>
#include <QDateTime>

class Namzy
{
public:
    explicit Namzy(quint64 seed = static_cast<quint64>(QDateTime::currentMSecsSinceEpoch()));

    QString generate();

private:
    QRandomGenerator m_rng;

    QString pickWord(const char* const* words, int count);
    static QString capitalize(const QString& s);
    QString fuse(const QString& first, const QString& second, quint16 activeMask);
};
