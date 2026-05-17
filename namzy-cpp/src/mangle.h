// this_file: namzy-cpp/src/mangle.h
#pragma once

#include <QString>
#include <QRandomGenerator>

QString applyRotation(const QString& s, QRandomGenerator& rng);
QString buildName(QRandomGenerator& rng);
