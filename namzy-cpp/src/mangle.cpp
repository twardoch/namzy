// this_file: namzy-cpp/src/mangle.cpp
#include "mangle.h"
#include "wordlist.h"
#include <QHash>

static QHash<QChar, QChar> buildRotationMap()
{
    QHash<QChar, QChar> m;
    for (const auto& p : namzy::rotations()) {
        m.insert(p.first, p.second);
    }
    return m;
}

static const QHash<QChar, QChar>& rotationMap()
{
    static const QHash<QChar, QChar> m = buildRotationMap();
    return m;
}

static void rotateAt(QString& s, int pos)
{
    if (pos < 0 || pos >= s.size()) return;
    const QChar ch = s.at(pos);
    const bool upper = ch.isUpper();
    const QChar lo = ch.toLower();
    auto it = rotationMap().find(lo);
    if (it == rotationMap().end()) return;
    s[pos] = upper ? it.value().toUpper() : it.value();
}

QString applyRotations(const QString& compound, QRandomGenerator& rng)
{
    if (compound.isEmpty()) return compound;
    QString out = compound;
    const int passes = (rng.bounded(2) == 0) ? 1 : 2;
    for (int i = 0; i < passes; ++i) {
        const int pos = static_cast<int>(rng.bounded(static_cast<quint32>(out.size())));
        rotateAt(out, pos);
    }
    return out;
}

static QString capitalize(const QString& s)
{
    if (s.isEmpty()) return s;
    return QString(s.at(0).toUpper()) + s.mid(1);
}

QString buildName(QRandomGenerator& rng)
{
    const QStringList& stems = namzy::stems();
    const int n = stems.size();
    const QString a = stems.at(static_cast<int>(rng.bounded(static_cast<quint32>(n))));
    const QString b = stems.at(static_cast<int>(rng.bounded(static_cast<quint32>(n))));
    return capitalize(applyRotations(a + b, rng));
}
