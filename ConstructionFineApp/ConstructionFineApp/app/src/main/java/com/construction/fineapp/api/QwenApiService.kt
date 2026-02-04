package com.construction.fineapp.api

import android.graphics.Bitmap
import android.util.Base64
import com.google.gson.Gson
import com.google.gson.JsonArray
import com.google.gson.JsonObject
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.ByteArrayOutputStream

data class ViolationAnalysis(
    val violation: String,
    val description: String,
    val suggestion: String
)

class QwenApiService(private val apiKey: String) {
    private val client = OkHttpClient()
    private val gson = Gson()

    suspend fun analyzeImage(bitmap: Bitmap): Result<ViolationAnalysis> = withContext(Dispatchers.IO) {
        try {
            // Convert bitmap to base64
            val outputStream = ByteArrayOutputStream()
            bitmap.compress(Bitmap.CompressFormat.JPEG, 80, outputStream)
            val imageBytes = outputStream.toByteArray()
            val base64Image = Base64.encodeToString(imageBytes, Base64.NO_WRAP)

            // Create request body for Qwen API
            val requestBody = JsonObject().apply {
                addProperty("model", "qwen-vl-plus")

                val input = JsonObject().apply {
                    val messages = JsonArray().apply {
                        add(JsonObject().apply {
                            addProperty("role", "user")

                            val content = JsonArray().apply {
                                // Image content
                                add(JsonObject().apply {
                                    addProperty("image", "data:image/jpeg;base64,$base64Image")
                                })

                                // Text content
                                add(JsonObject().apply {
                                    addProperty("text", """
                                        请分析这张施工现场的照片，识别出违规操作。
                                        请以JSON格式返回，格式如下：
                                        {
                                            "violation": "违规类型（如：没戴安全帽、脚手架不稳等）",
                                            "description": "详细说明违规情况",
                                            "suggestion": "整改建议"
                                        }
                                        只返回JSON，不要其他文字。
                                    """.trimIndent())
                                })
                            }

                            add("content", content)
                        })
                    }

                    add("messages", messages)
                }

                add("input", input)

                // Add parameters
                val parameters = JsonObject().apply {
                    addProperty("result_format", "message")
                }

                add("parameters", parameters)
            }.toString()

            val request = Request.Builder()
                .url("https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation")
                .addHeader("Authorization", "Bearer $apiKey")
                .addHeader("Content-Type", "application/json")
                .post(requestBody.toRequestBody("application/json".toMediaType()))
                .build()

            val response = client.newCall(request).execute()
            val responseBody = response.body?.string()

            if (response.isSuccessful && responseBody != null) {
                val jsonResponse = gson.fromJson(responseBody, JsonObject::class.java)
                val content = jsonResponse
                    .getAsJsonObject("output")
                    .getAsJsonArray("choices")
                    .get(0).asJsonObject
                    .getAsJsonObject("message")
                    .getAsJsonArray("content")
                    .get(0).asJsonObject
                    .get("text").asString

                // Parse JSON response from AI
                // Find JSON in the response (in case there's extra text)
                val jsonPattern = Regex("""\{[^{}]*"violation"[^{}]*"description"[^{}]*"suggestion"[^{}]*\}""")
                val match = jsonPattern.find(content)

                if (match != null) {
                    val jsonStr = match.value
                    val analysisJson = gson.fromJson(jsonStr, JsonObject::class.java)
                    val analysis = ViolationAnalysis(
                        violation = analysisJson.get("violation").asString,
                        description = analysisJson.get("description").asString,
                        suggestion = analysisJson.get("suggestion").asString
                    )

                    Result.success(analysis)
                } else {
                    // If JSON parsing fails, create a default response
                    Result.failure(Exception("无法解析AI返回的JSON格式: $content"))
                }
            } else {
                Result.failure(Exception("API调用失败: ${response.code} - $responseBody"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
