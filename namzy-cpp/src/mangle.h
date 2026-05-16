// this_file: namzy-cpp/src/mangle.h
#pragma once

#include <QString>
#include <QtGlobal>

quint16 allRotationRules();
QString mangle(const QString& word, quint16 activeMask = allRotationRules());
QString joinClean(const QString& a, const QString& b);
