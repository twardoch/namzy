// this_file: namzy-cpp/src/mangle.h
#pragma once

#include <QString>
#include <QRandomGenerator>

QString applyRotations(const QString& compound, QRandomGenerator& rng);
QString buildName(QRandomGenerator& rng);
