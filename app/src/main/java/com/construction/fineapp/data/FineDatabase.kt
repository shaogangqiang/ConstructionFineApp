package com.construction.fineapp.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [FineRecord::class], version = 1)
abstract class FineDatabase : RoomDatabase() {
    abstract fun fineDao(): FineDao

    companion object {
        @Volatile
        private var INSTANCE: FineDatabase? = null

        fun getDatabase(context: Context): FineDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    FineDatabase::class.java,
                    "fine_database"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}
