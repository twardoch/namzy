// this_file: namzy-cpp/src/namzy.h
#pragma once

#include <QString>
#include <QStringList>
#include <QRandomGenerator>
#include <QDateTime>

class Namzy
{
public:
    explicit Namzy(quint64 seed = static_cast<quint64>(QDateTime::currentMSecsSinceEpoch()));

    QString generate();
    QStringList generateMany(int count);

private:
    QRandomGenerator m_rng;
};
