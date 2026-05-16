// this_file: namzy-cpp/src/namzy.cpp
#include "namzy.h"
#include "wordlist.h"
#include "mangle.h"
#include <QVector>


Namzy::Namzy(quint64 seed)
    : m_rng(seed)
{
}

QString Namzy::capitalize(const QString& s)
{
    if (s.isEmpty()) return s;
    return s.at(0).toUpper() + s.mid(1).toLower();
}

QString Namzy::pickWord(const char* const* words, int count)
{
    int idx = static_cast<int>(m_rng.bounded(static_cast<quint32>(count)));
    return QString::fromLatin1(words[idx]);
}

QString Namzy::fuse(const QString& first, const QString& second, quint16 activeMask)
{
    const QString fused = joinClean(first.toLower(), second.toLower());
    const QString mangled = mangle(fused, activeMask);
    return capitalize(mangled);
}

QString Namzy::generate()
{
    QString geo    = pickWord(Wordlist::GEO_WORDS,    Wordlist::GEO_COUNT);
    QString common = pickWord(Wordlist::COMMON_WORDS, Wordlist::COMMON_COUNT);
    quint16 activeMask = 0;
    const int activeCount = static_cast<int>(m_rng.bounded(10)) + 1;
    QVector<int> order;
    order.reserve(10);
    for (int i = 0; i < 10; ++i) order.append(i);
    for (int i = 0; i < activeCount; ++i) {
        const int swap = i + static_cast<int>(m_rng.bounded(static_cast<quint32>(order.size() - i)));
        order.swapItemsAt(i, swap);
        activeMask |= static_cast<quint16>(1U << order.at(i));
    }
    if (m_rng.bounded(2) == 0) {
        return fuse(geo, common, activeMask);
    }
    return fuse(common, geo, activeMask);
}
